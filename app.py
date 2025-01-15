from flask import Flask
from utils.Database import db
from config.DatabaseConfig import DatabaseConfig
from models.UsersModel import UsersModel
from models.PersonalDataModel import PersonalDataModel
from controllers.RestPersonalDataController import rest_personal_data_controller

app = Flask(__name__)

# Initialize database config
db_config = DatabaseConfig(app)

# Register the Blueprint
app.register_blueprint(rest_personal_data_controller)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
