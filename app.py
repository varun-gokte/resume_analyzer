from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from routes import main
from dotenv import load_dotenv

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@localhost:{db_port}/{db_name}"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR,'uploads')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main)
    
    return app

app = create_app()
if __name__=='__main__':
    app.run(debug=True)