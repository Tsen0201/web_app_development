"""
任務管理系統 — 路由模組初始化

註冊所有 Blueprint 到 Flask app。
"""


def register_routes(app):
    """
    將所有 Blueprint 註冊到 Flask 應用程式。

    Args:
        app: Flask 應用程式實例。
    """
    from app.routes.pages import pages_bp
    from app.routes.tasks import tasks_bp
    from app.routes.categories import categories_bp
    from app.routes.api import api_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(api_bp)
