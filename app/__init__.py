import os
import sqlite3
from flask import Flask

def create_app():
    # 初始化 Flask 應用程式
    app = Flask(__name__)
    
    # 載入環境變數設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 設定圖片上傳的資料夾路徑
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder
    
    # 註冊 Blueprints (路由)
    from app.routes.index import index_bp
    from app.routes.recipe import recipe_bp
    
    app.register_blueprint(index_bp)
    app.register_blueprint(recipe_bp)
    
    return app

def init_db():
    """初始化資料庫（首次執行時建立資料表）"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_folder = os.path.join(base_dir, 'instance')
    os.makedirs(db_folder, exist_ok=True)
    
    db_path = os.path.join(db_folder, 'database.db')
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print("Database initialised successfully at instance/database.db")
