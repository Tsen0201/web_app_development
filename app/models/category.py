"""
Category Model — 分類資料的 CRUD 操作

提供分類（Category）資料表的新增、查詢、更新、刪除方法。
使用 sqlite3 直接操作資料庫，每個函式皆包含錯誤處理。
"""

from app.models import get_db


def create(name):
    """
    建立一個新分類。

    Args:
        name (str): 分類名稱（不可重複）。

    Returns:
        int | None: 新建立分類的 id，失敗時回傳 None。
    """
    db = None
    try:
        db = get_db()
        cursor = db.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )
        db.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"[Category.create] 錯誤：{e}")
        if db:
            db.rollback()
        return None
    finally:
        if db:
            db.close()


def get_all():
    """
    取得所有分類。

    Returns:
        list[dict]: 所有分類的列表，失敗時回傳空列表。
    """
    db = None
    try:
        db = get_db()
        rows = db.execute(
            "SELECT * FROM categories ORDER BY id ASC"
        ).fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[Category.get_all] 錯誤：{e}")
        return []
    finally:
        if db:
            db.close()


def get_by_id(category_id):
    """
    依 ID 取得單一分類。

    Args:
        category_id (int): 分類 ID。

    Returns:
        dict | None: 分類資料，或 None（若不存在或發生錯誤）。
    """
    db = None
    try:
        db = get_db()
        row = db.execute(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"[Category.get_by_id] 錯誤：{e}")
        return None
    finally:
        if db:
            db.close()


def update(category_id, name):
    """
    更新指定分類的名稱。

    Args:
        category_id (int): 分類 ID。
        name (str): 新的分類名稱。

    Returns:
        bool: 是否成功更新（True 表示有找到並更新）。
    """
    db = None
    try:
        db = get_db()
        cursor = db.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (name, category_id)
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"[Category.update] 錯誤：{e}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            db.close()


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
    db = None
    try:
        db = get_db()
        cursor = db.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"[Category.delete] 錯誤：{e}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            db.close()
