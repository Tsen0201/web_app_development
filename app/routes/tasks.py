"""
任務路由 — 任務的 CRUD 操作

處理任務的新增、檢視、編輯、更新、刪除與狀態切換。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks/new')
def new_task():
    """
    新增任務頁面。

    - 呼叫 category.get_all() 取得分類選項
    - 渲染 task_form.html，task=None 表示新增模式
    """
    # TODO: 實作
    pass


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    建立任務。

    - 接收表單欄位：title(必填), description, due_date,
      category_id, reminder_at, recurrence
    - 驗證 title 不為空
    - 呼叫 task.create(...) 寫入資料庫
    - 重導向至 /
    - 錯誤時 flash 訊息並重新渲染表單
    """
    # TODO: 實作
    pass


@tasks_bp.route('/tasks/<int:task_id>')
def task_detail(task_id):
    """
    任務詳情頁面。

    - 呼叫 task.get_by_id(task_id) 取得任務資料
    - 渲染 task_detail.html
    - 找不到時回傳 404
    """
    # TODO: 實作
    pass


@tasks_bp.route('/tasks/<int:task_id>/edit')
def edit_task(task_id):
    """
    編輯任務頁面。

    - 呼叫 task.get_by_id(task_id) 取得現有任務資料
    - 呼叫 category.get_all() 取得分類選項
    - 渲染 task_form.html（編輯模式）
    - 找不到時回傳 404
    """
    # TODO: 實作
    pass


@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    更新任務。

    - 接收表單欄位同 create_task
    - 驗證 title 不為空
    - 呼叫 task.update(task_id, ...) 更新資料庫
    - 重導向至 /
    - 找不到時回傳 404；驗證失敗時 flash 錯誤
    """
    # TODO: 實作
    pass


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務。

    - 呼叫 task.delete(task_id) 從資料庫移除
    - 重導向至 /
    - 找不到時回傳 404
    """
    # TODO: 實作
    pass


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務狀態（pending ↔ completed）。

    - 呼叫 task.toggle_status(task_id)
    - 重導向至 /
    - 找不到時回傳 404
    """
    # TODO: 實作
    pass
