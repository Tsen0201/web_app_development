"""
頁面路由 — 首頁與月曆檢視

處理主要瀏覽頁面的路由邏輯。
"""

import calendar as cal
from datetime import datetime

from flask import Blueprint, render_template, request

from app.models import task, category

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """
    首頁 — 任務列表看板。

    - 顯示所有任務（可依分類篩選）
    - 呼叫 task.get_all() 或 task.get_by_category()
    - 呼叫 category.get_all() 供篩選下拉選單
    - 渲染 index.html
    """
    # 取得篩選參數
    filter_category = request.args.get('category', type=int)

    # 依篩選條件取得任務
    if filter_category:
        tasks = task.get_by_category(filter_category)
    else:
        tasks = task.get_all()

    # 取得所有分類（供篩選下拉選單）
    categories = category.get_all()

    return render_template(
        'index.html',
        tasks=tasks,
        categories=categories,
        filter_category=filter_category
    )


@pages_bp.route('/calendar')
def calendar_view():
    """
    月曆檢視頁面。

    - 接收可選參數 ?year=YYYY&month=MM（預設為當月）
    - 呼叫 task.get_by_month(year, month) 取得該月任務
    - 組裝月曆資料結構
    - 渲染 calendar.html
    """
    now = datetime.now()

    # 解析年月參數，預設為當前年月
    try:
        year = request.args.get('year', now.year, type=int)
        month = request.args.get('month', now.month, type=int)

        # 邊界檢查
        if month < 1 or month > 12:
            year, month = now.year, now.month
    except (ValueError, TypeError):
        year, month = now.year, now.month

    # 計算上個月與下個月（用於翻頁按鈕）
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    # 取得該月任務
    month_tasks = task.get_by_month(year, month)

    # 組裝月曆資料結構：{日期: [任務列表]}
    tasks_by_date = {}
    for t in month_tasks:
        if t.get('due_date'):
            try:
                date_key = t['due_date'][:10]  # 取 YYYY-MM-DD
                day = int(date_key.split('-')[2])
                if day not in tasks_by_date:
                    tasks_by_date[day] = []
                tasks_by_date[day].append(t)
            except (ValueError, IndexError):
                pass

    # 取得該月的日曆資訊
    month_calendar = cal.monthcalendar(year, month)
    month_name = f"{year} 年 {month} 月"

    return render_template(
        'calendar.html',
        year=year,
        month=month,
        month_name=month_name,
        month_calendar=month_calendar,
        tasks_by_date=tasks_by_date,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        today=now.day if year == now.year and month == now.month else None
    )
