"""
任務管理系統 — Flask 應用程式初始化

建立並設定 Flask app 實例，初始化資料庫與註冊路由。
"""

import os
from flask import Flask


def create_app():
    """
    Flask Application Factory。

    建立 Flask app 實例並完成以下設定：
    1. 設定 SECRET_KEY（flash message 需要）
    2. 設定 instance 資料夾路徑
    3. 初始化資料庫
    4. 註冊所有 Blueprint 路由
    """
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='templates',
        static_folder='static'
    )

    # 設定 SECRET_KEY（用於 session 與 flash message）
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化資料庫（建表）
    from app.models import init_db
    init_db()

    # 註冊路由
    from app.routes import register_routes
    register_routes(app)

    return app
