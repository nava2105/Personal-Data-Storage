from flask import Blueprint, jsonify, request
from services.AuthService import AuthService
from factories.MySQLDatabaseFactory import MySQLDatabaseFactory
from utils.Database import db
import os

# Initialize a Blueprint for the controller
rest_personal_data_controller = Blueprint('rest_personal_data_controller', __name__)

# Retrieve the database factory instance
db_factory = MySQLDatabaseFactory(db)


@rest_personal_data_controller.route('/', methods=['GET'])
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
    with rest_personal_data_controller.app_context():
        user_repository = db_factory.get_user_repository()
        user_data = user_repository.get_user_by_id(user_id)
        if not user_data:
            return jsonify({"error": f"No user found with ID {user_id}"}), 404
        return jsonify(user_data), 200


@rest_personal_data_controller.route('/register/personal/data', methods=['POST'])
def register_personal_data():
    """Endpoint to register personal data for a user."""
    auth_header = request.headers.get('Authorization')
    user_id, dto, existing_personal_data, error_response = AuthService.get_user_and_personal_data(auth_header, request,
                                                                                                  db_factory)
    if error_response:
        return error_response, 400
    if existing_personal_data:
        return jsonify({"error": "Personal data is already registered for this user"}), 401
    try:
        with rest_personal_data_controller.app_context():
            personal_data_repository = db_factory.get_personal_data_repository()
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


@rest_personal_data_controller.route('/modify/personal/data', methods=['POST'])
def modify_personal_data():
    """Endpoint to modify personal data for a user."""
    auth_header = request.headers.get('Authorization')
    user_id, dto, existing_personal_data, error_response = AuthService.get_user_and_personal_data(auth_header, request,
                                                                                                  db_factory)
    if error_response:
        return error_response, 401
    if not existing_personal_data:
        return jsonify({"error": "Personal data is not registered for this user"}), 400
    try:
        with rest_personal_data_controller.app_context():
            personal_data_repository = db_factory.get_personal_data_repository()
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


@rest_personal_data_controller.route('/get/personal/data', methods=['GET'])
def get_personal_data():
    """Endpoint to get personal data for a user."""
    auth_header = request.headers.get('Authorization')
    try:
        user_id = AuthService.authenticate_user(auth_header)
        personal_data_repository = db_factory.get_personal_data_repository()
        existing_personal_data = personal_data_repository.get_personal_data_by_user_id(user_id)
        if not existing_personal_data:
            return jsonify({"error": "No personal data found"}), 404
        return jsonify(existing_personal_data[0]), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400