"""
Task Model — 任務資料的 CRUD 操作與查詢邏輯
"""

from app.models import get_db


def create(title, description='', status='pending', due_date=None,
           category_id=None, reminder_at=None, recurrence='none'):
    """
    建立一個新任務。

    Args:
        title (str): 任務標題（必填）。
        description (str): 任務描述。
        status (str): 狀態，預設 'pending'。
        due_date (str|None): 截止日期時間（ISO 8601）。
        category_id (int|None): 所屬分類 ID。
        reminder_at (str|None): 提醒時間（ISO 8601）。
        recurrence (str): 重複週期，預設 'none'。

    Returns:
        int: 新建立任務的 id。
    """
    db = get_db()
    cursor = db.execute(
        """INSERT INTO tasks (title, description, status, due_date,
                              category_id, reminder_at, recurrence)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (title, description, status, due_date,
         category_id, reminder_at, recurrence)
    )
    db.commit()
    new_id = cursor.lastrowid
    db.close()
    return new_id


def get_all():
    """
    取得所有任務（依截止日期排序，NULL 排最後）。

    Returns:
        list[dict]: 所有任務的列表。
    """
    db = get_db()
    rows = db.execute(
        """SELECT t.*, c.name AS category_name
           FROM tasks t
           LEFT JOIN categories c ON t.category_id = c.id
           ORDER BY t.due_date IS NULL, t.due_date ASC, t.created_at DESC"""
    ).fetchall()
    db.close()
    return [dict(row) for row in rows]


def get_by_id(task_id):
    """
    依 ID 取得單一任務。

    Args:
        task_id (int): 任務 ID。

    Returns:
        dict | None: 任務資料（含分類名稱），或 None。
    """
    db = get_db()
    row = db.execute(
        """SELECT t.*, c.name AS category_name
           FROM tasks t
           LEFT JOIN categories c ON t.category_id = c.id
           WHERE t.id = ?""",
        (task_id,)
    ).fetchone()
    db.close()
    return dict(row) if row else None


def update(task_id, title=None, description=None, status=None,
           due_date=None, category_id=None, reminder_at=None,
           recurrence=None):
    """
    更新指定任務的欄位。只會更新有傳入值的欄位。

    Args:
        task_id (int): 任務 ID。
        title (str|None): 新標題。
        description (str|None): 新描述。
        status (str|None): 新狀態。
        due_date (str|None): 新截止日期。
        category_id (int|None): 新分類 ID。
        reminder_at (str|None): 新提醒時間。
        recurrence (str|None): 新重複週期。

    Returns:
        bool: 是否成功更新。
    """
    fields = []
    values = []

    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if status is not None:
        fields.append("status = ?")
        values.append(status)
    if due_date is not None:
        fields.append("due_date = ?")
        values.append(due_date)
    if category_id is not None:
        fields.append("category_id = ?")
        values.append(category_id)
    if reminder_at is not None:
        fields.append("reminder_at = ?")
        values.append(reminder_at)
    if recurrence is not None:
        fields.append("recurrence = ?")
        values.append(recurrence)

    if not fields:
        return False

    # 自動更新 updated_at
    fields.append("updated_at = datetime('now', 'localtime')")

    values.append(task_id)

    sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"

    db = get_db()
    cursor = db.execute(sql, values)
    db.commit()
    affected = cursor.rowcount
    db.close()
    return affected > 0


def delete(task_id):
    """
    刪除指定任務。

    Args:
        task_id (int): 任務 ID。

    Returns:
        bool: 是否成功刪除。
    """
    db = get_db()
    cursor = db.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    db.commit()
    affected = cursor.rowcount
    db.close()
    return affected > 0


def toggle_status(task_id):
    """
    切換指定任務的完成狀態（pending ↔ completed）。

    Args:
        task_id (int): 任務 ID。

    Returns:
        str | None: 切換後的新狀態，或 None（若找不到任務）。
    """
    db = get_db()
    row = db.execute(
        "SELECT status FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if not row:
        db.close()
        return None

    new_status = 'completed' if row['status'] == 'pending' else 'pending'
    db.execute(
        """UPDATE tasks
           SET status = ?, updated_at = datetime('now', 'localtime')
           WHERE id = ?""",
        (new_status, task_id)
    )
    db.commit()
    db.close()
    return new_status


def get_by_date(date_str):
    """
    依日期查詢任務（月曆功能用）。

    Args:
        date_str (str): 日期字串，格式為 'YYYY-MM-DD'。

    Returns:
        list[dict]: 該日期的任務列表。
    """
    db = get_db()
    rows = db.execute(
        """SELECT t.*, c.name AS category_name
           FROM tasks t
           LEFT JOIN categories c ON t.category_id = c.id
           WHERE date(t.due_date) = ?
           ORDER BY t.due_date ASC""",
        (date_str,)
    ).fetchall()
    db.close()
    return [dict(row) for row in rows]


def get_by_category(category_id):
    """
    依分類查詢任務。

    Args:
        category_id (int): 分類 ID。

    Returns:
        list[dict]: 該分類下的任務列表。
    """
    db = get_db()
    rows = db.execute(
        """SELECT t.*, c.name AS category_name
           FROM tasks t
           LEFT JOIN categories c ON t.category_id = c.id
           WHERE t.category_id = ?
           ORDER BY t.due_date IS NULL, t.due_date ASC""",
        (category_id,)
    ).fetchall()
    db.close()
    return [dict(row) for row in rows]


def get_by_month(year, month):
    """
    依年月查詢任務（月曆整月顯示用）。

    Args:
        year (int): 年份。
        month (int): 月份 (1-12)。

    Returns:
        list[dict]: 該月份的所有任務。
    """
    date_prefix = f"{year:04d}-{month:02d}"
    db = get_db()
    rows = db.execute(
        """SELECT t.*, c.name AS category_name
           FROM tasks t
           LEFT JOIN categories c ON t.category_id = c.id
           WHERE t.due_date LIKE ?
           ORDER BY t.due_date ASC""",
        (date_prefix + '%',)
    ).fetchall()
    db.close()
    return [dict(row) for row in rows]


def get_pending_reminders():
    """
    取得所有設有提醒且尚未完成的任務（提醒功能用）。

    Returns:
        list[dict]: 需要提醒的任務列表。
    """
    db = get_db()
    rows = db.execute(
        """SELECT t.*, c.name AS category_name
           FROM tasks t
           LEFT JOIN categories c ON t.category_id = c.id
           WHERE t.status = 'pending'
             AND t.reminder_at IS NOT NULL
           ORDER BY t.reminder_at ASC"""
    ).fetchall()
    db.close()
    return [dict(row) for row in rows]
