from flask import Flask
import os
from .main import main
from dotenv import load_dotenv
from app.extensions import db, migrate

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR,'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    
    return app