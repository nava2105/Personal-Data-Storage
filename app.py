from flask import Flask, jsonify, request
from utils.Database import db
from config.DatabaseConfig import DatabaseConfig
from dotenv import load_dotenv
import requests
from factories.MySQLDatabaseFactory import MySQLDatabaseFactory
import os
from models.UsersModel import UsersModel
from models.PersonalDataModel import PersonalDataModel
from dtos.DtoPersonalData import DtoPersonalData

app = Flask(__name__)

# Initialize database config
db_config = DatabaseConfig(app)

# Initialize factory
db_factory = MySQLDatabaseFactory(db)

load_dotenv()

@app.route('/')
def home():
    """Home endpoint to get user data from the token."""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header is required"}), 401
    auth_url = os.getenv('AUTH_URL')
    auth_url = f"{auth_url}/user_id/token"
    response = requests.get(auth_url, headers={"Authorization": auth_header})
    if response.status_code != 200:
        return jsonify({"error": "Invalid authorization"}), response.status_code
    user_id = response.json().get('userId')
    if not user_id:
        return jsonify({"error": "User ID not found in API response"}), 400
    with app.app_context():
        user_repository = db_factory.get_user_repository()
        user_data = user_repository.get_user_by_id(user_id)
        if not user_data:
            return jsonify({"error": f"No user found with ID {user_id}"}), 404
        return jsonify(user_data)

@app.route('/register/personal/data', methods=['POST'])
def register_personal_data():
    """Endpoint to register personal data for a user."""
    try:
        user_id = authenticate_user(request.headers.get('Authorization'))
        data = request.get_json()
        try:
            dto = DtoPersonalData.from_json(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        personal_data_repository = db_factory.get_personal_data_repository()
        existing_personal_data = personal_data_repository.get_personal_data_by_user_id(user_id)
        if existing_personal_data:
            return jsonify({"error": "Personal data is already registered for this user"}), 400
        with app.app_context():
            personal_data_repository.create_personal_data(
                user_id=user_id,
                birth_date=dto.birth_date,
                height=dto.height,
                weight=dto.weight,
                body_structure=dto.body_structure
            )
        return jsonify({"message": "Personal data registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/modify/personal/data', methods=['POST'])
def modify_personal_data():
    """Endpoint to modify personal data for a user."""
    try:
        user_id = authenticate_user(request.headers.get('Authorization'))
        data = request.get_json()
        try:
            dto = DtoPersonalData.from_json(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        personal_data_repository = db_factory.get_personal_data_repository()
        existing_personal_data = personal_data_repository.get_personal_data_by_user_id(user_id)
        if not existing_personal_data:
            return jsonify({"error": "Personal data is not registered for this user"}), 400
        with app.app_context():
            personal_data_repository.update_personal_data(
                user_id=user_id,
                birth_date=dto.birth_date,
                height=dto.height,
                weight=dto.weight,
                body_structure=dto.body_structure
            )
        return jsonify({"message": "Personal data modified successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def authenticate_user(auth_header):
    """Authenticate user and return user_id."""
    if not auth_header:
        raise Exception("Authorization header is required")
    auth_url = os.getenv('AUTH_URL')
    response = requests.get(f"{auth_url}/user_id/token", headers={"Authorization": auth_header})
    if response.status_code != 200:
        raise Exception("Invalid authorization")
    user_id = response.json().get('userId')
    if not user_id:
        raise Exception("User ID not found in token response")
    return user_id


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
