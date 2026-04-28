"""
分類路由 — 分類的管理操作

處理分類的列表顯示、新增與刪除。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/categories')
def category_list():
    """
    分類列表頁面。

    - 呼叫 category.get_all() 取得所有分類
    - 渲染 categories.html
    """
    # TODO: 實作
    pass


@categories_bp.route('/categories', methods=['POST'])
def create_category():
    """
    建立分類。

    - 接收表單欄位：name(必填)
    - 驗證 name 不為空且不重複
    - 呼叫 category.create(name) 寫入資料庫
    - 重導向至 /categories
    - 錯誤時 flash 訊息
    """
    # TODO: 實作
    pass


@categories_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """
    刪除分類。

    - 呼叫 category.delete(category_id) 從資料庫移除
    - 該分類下的任務的 category_id 會自動設為 NULL
    - 重導向至 /categories
    - 找不到時回傳 404
    """
    # TODO: 實作
    pass
