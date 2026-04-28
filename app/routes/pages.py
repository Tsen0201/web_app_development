"""
頁面路由 — 首頁與月曆檢視

處理主要瀏覽頁面的路由邏輯。
"""

from flask import Blueprint, render_template, request

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """
    首頁 — 任務列表看板。

    - 顯示所有任務（可依分類篩選）
    - 顯示今日待提醒任務
    - 呼叫 task.get_all() 或 task.get_by_category()
    - 呼叫 category.get_all() 供篩選下拉選單
    - 渲染 index.html
    """
    # TODO: 實作
    pass


@pages_bp.route('/calendar')
def calendar():
    """
    月曆檢視頁面。

    - 接收可選參數 ?year=YYYY&month=MM（預設為當月）
    - 呼叫 task.get_by_month(year, month) 取得該月任務
    - 組裝月曆資料結構
    - 渲染 calendar.html
    """
    # TODO: 實作
    pass
