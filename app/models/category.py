"""
Category Model — 分類資料的 CRUD 操作
"""

from app.models import get_db


def create(name):
    """
    建立一個新分類。

    Args:
        name (str): 分類名稱（不可重複）。

    Returns:
        int: 新建立分類的 id。
    """
    db = get_db()
    cursor = db.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (name,)
    )
    db.commit()
    new_id = cursor.lastrowid
    db.close()
    return new_id


def get_all():
    """
    取得所有分類。

    Returns:
        list[dict]: 所有分類的列表。
    """
    db = get_db()
    rows = db.execute(
        "SELECT * FROM categories ORDER BY id ASC"
    ).fetchall()
    db.close()
    return [dict(row) for row in rows]


def get_by_id(category_id):
    """
    依 ID 取得單一分類。

    Args:
        category_id (int): 分類 ID。

    Returns:
        dict | None: 分類資料，或 None（若不存在）。
    """
    db = get_db()
    row = db.execute(
        "SELECT * FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()
    db.close()
    return dict(row) if row else None


def update(category_id, name):
    """
    更新指定分類的名稱。

    Args:
        category_id (int): 分類 ID。
        name (str): 新的分類名稱。

    Returns:
        bool: 是否成功更新（True 表示有找到並更新）。
    """
    db = get_db()
    cursor = db.execute(
        "UPDATE categories SET name = ? WHERE id = ?",
        (name, category_id)
    )
    db.commit()
    affected = cursor.rowcount
    db.close()
    return affected > 0


def delete(category_id):
    """
    刪除指定分類。

    刪除後，該分類下的任務的 category_id 會被設為 NULL
    （由資料庫 ON DELETE SET NULL 約束處理）。

    Args:
        category_id (int): 分類 ID。

    Returns:
        bool: 是否成功刪除。
    """
    db = get_db()
    cursor = db.execute(
        "DELETE FROM categories WHERE id = ?",
        (category_id,)
    )
    db.commit()
    affected = cursor.rowcount
    db.close()
    return affected > 0
