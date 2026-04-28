"""
分類路由 — 分類的管理操作

處理分類的列表顯示、新增與刪除。
使用 Flask Blueprint 組織路由，表單驗證失敗時使用 flash message 顯示錯誤。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.models import category

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/categories')
def category_list():
    """
    分類列表頁面。

    - 呼叫 category.get_all() 取得所有分類
    - 渲染 categories.html
    """
    categories = category.get_all()
    return render_template('categories.html', categories=categories)


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
    name = request.form.get('name', '').strip()

    # 驗證名稱不為空
    if not name:
        flash('分類名稱不可為空！', 'error')
        return redirect(url_for('categories.category_list'))

    # 檢查是否重複
    existing = category.get_all()
    if any(c['name'] == name for c in existing):
        flash(f'分類「{name}」已經存在！', 'error')
        return redirect(url_for('categories.category_list'))

    # 寫入資料庫
    new_id = category.create(name)

    if new_id:
        flash(f'分類「{name}」新增成功！', 'success')
    else:
        flash('分類新增失敗，請稍後再試。', 'error')

    return redirect(url_for('categories.category_list'))


@categories_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """
    刪除分類。

    - 呼叫 category.delete(category_id) 從資料庫移除
    - 該分類下的任務的 category_id 會自動設為 NULL
    - 重導向至 /categories
    - 找不到時回傳 404
    """
    cat = category.get_by_id(category_id)
    if not cat:
        abort(404)

    success = category.delete(category_id)

    if success:
        flash(f'分類「{cat["name"]}」已刪除。', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'error')

    return redirect(url_for('categories.category_list'))
