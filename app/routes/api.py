"""
API 路由 — 提供 JSON 格式資料

供前端 JavaScript（月曆點擊、提醒通知）使用的 API 端點。
"""

from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/tasks')
def get_tasks_by_date():
    """
    查詢特定日期的任務（JSON）。

    - 接收 query param: date=YYYY-MM-DD
    - 呼叫 task.get_by_date(date) 查詢該日任務
    - 回傳 JSON { "tasks": [...] }
    - 缺少 date 參數時回傳 400
    """
    # TODO: 實作
    pass


@api_bp.route('/api/reminders')
def get_reminders():
    """
    查詢待提醒任務（JSON）。

    - 呼叫 task.get_pending_reminders() 取得所有待提醒任務
    - 回傳 JSON { "reminders": [...] }
    """
    # TODO: 實作
    pass
