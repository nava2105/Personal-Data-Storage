import os

from utils.db import db
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    def __init__(self, app):
        db_ip = os.getenv('DB_IP')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True

        db.init_app(app)

    @staticmethod
    def get_db():
        return db
