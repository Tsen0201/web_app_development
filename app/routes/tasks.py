"""
任務路由 — 任務的 CRUD 操作

處理任務的新增、檢視、編輯、更新、刪除與狀態切換。
使用 Flask Blueprint 組織路由，表單驗證失敗時使用 flash message 顯示錯誤。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.models import task, category

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks/new')
def new_task():
    """
    新增任務頁面。

    - 呼叫 category.get_all() 取得分類選項
    - 渲染 task_form.html，task=None 表示新增模式
    """
    categories = category.get_all()
    return render_template(
        'task_form.html',
        task=None,
        categories=categories
    )


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
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip() or None
    category_id = request.form.get('category_id', type=int) or None
    reminder_at = request.form.get('reminder_at', '').strip() or None
    recurrence = request.form.get('recurrence', 'none').strip()

    # 驗證必填欄位
    if not title:
        flash('任務標題不可為空！', 'error')
        categories = category.get_all()
        return render_template(
            'task_form.html',
            task=None,
            categories=categories
        )

    # 寫入資料庫
    new_id = task.create(
        title=title,
        description=description,
        due_date=due_date,
        category_id=category_id,
        reminder_at=reminder_at,
        recurrence=recurrence
    )

    if new_id:
        flash('任務新增成功！', 'success')
    else:
        flash('任務新增失敗，請稍後再試。', 'error')

    return redirect(url_for('pages.index'))


@tasks_bp.route('/tasks/<int:task_id>')
def task_detail(task_id):
    """
    任務詳情頁面。

    - 呼叫 task.get_by_id(task_id) 取得任務資料
    - 渲染 task_detail.html
    - 找不到時回傳 404
    """
    t = task.get_by_id(task_id)
    if not t:
        abort(404)

    return render_template('task_detail.html', task=t)


@tasks_bp.route('/tasks/<int:task_id>/edit')
def edit_task(task_id):
    """
    編輯任務頁面。

    - 呼叫 task.get_by_id(task_id) 取得現有任務資料
    - 呼叫 category.get_all() 取得分類選項
    - 渲染 task_form.html（編輯模式）
    - 找不到時回傳 404
    """
    t = task.get_by_id(task_id)
    if not t:
        abort(404)

    categories = category.get_all()
    return render_template(
        'task_form.html',
        task=t,
        categories=categories
    )


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
    # 確認任務存在
    t = task.get_by_id(task_id)
    if not t:
        abort(404)

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip() or None
    category_id = request.form.get('category_id', type=int) or None
    reminder_at = request.form.get('reminder_at', '').strip() or None
    recurrence = request.form.get('recurrence', 'none').strip()

    # 驗證必填欄位
    if not title:
        flash('任務標題不可為空！', 'error')
        categories = category.get_all()
        return render_template(
            'task_form.html',
            task=t,
            categories=categories
        )

    # 更新資料庫
    success = task.update(
        task_id,
        title=title,
        description=description,
        due_date=due_date,
        category_id=category_id,
        reminder_at=reminder_at,
        recurrence=recurrence
    )

    if success:
        flash('任務更新成功！', 'success')
    else:
        flash('任務更新失敗，請稍後再試。', 'error')

    return redirect(url_for('pages.index'))


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務。

    - 呼叫 task.delete(task_id) 從資料庫移除
    - 重導向至 /
    - 找不到時回傳 404
    """
    t = task.get_by_id(task_id)
    if not t:
        abort(404)

    success = task.delete(task_id)

    if success:
        flash('任務已刪除。', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'error')

    return redirect(url_for('pages.index'))


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務狀態（pending ↔ completed）。

    - 呼叫 task.toggle_status(task_id)
    - 重導向至 /
    - 找不到時回傳 404
    """
    new_status = task.toggle_status(task_id)

    if new_status is None:
        abort(404)

    status_text = '已完成' if new_status == 'completed' else '未完成'
    flash(f'任務狀態已切換為「{status_text}」。', 'success')

    return redirect(url_for('pages.index'))
