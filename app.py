from flask import Flask, jsonify, request
from utils.Database import db
from config.DatabaseConfig import DatabaseConfig
from dotenv import load_dotenv
import requests
from factories.MySQLDatabaseFactory import MySQLDatabaseFactory
import os
from models.UsersModel import UsersModel
from models.PersonalDataModel import PersonalDataModel
from dtos.DtoPersonalData import DtoRegisterPersonalData

app = Flask(__name__)

# Initialize database config
db_config = DatabaseConfig(app)

# Initialize factory
db_factory = MySQLDatabaseFactory(db)

load_dotenv()

@app.route('/')
def home():
    # Check if the Authorization header is present
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header is required"}), 401

    # Send the Authorization header to the external API
    auth_url = os.getenv('AUTH_URL')
    auth_url = f"{auth_url}/user_id/token"
    response = requests.get(auth_url, headers={"Authorization": auth_header})

    # Check if the external API call was successful
    if response.status_code != 200:
        return jsonify({"error": "Invalid authorization"}), response.status_code

    # Extract user ID from the external API response
    user_id = response.json().get('userId')
    if not user_id:
        return jsonify({"error": "User ID not found in API response"}), 400

    # Query the database for the given user_id
    with app.app_context():
        user_repository = db_factory.get_user_repository()
        user_data = user_repository.get_user_by_id(user_id)

        # If no user is found, return an error
        if not user_data:
            return jsonify({"error": f"No user found with ID {user_id}"}), 404

        return jsonify(user_data)


@app.route('/register/personal/data', methods=['POST'])
def register_personal_data():
    """Endpoint to get all users using the abstract factory."""
    try:
        # Validate the Authorization token
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is required"}), 401

        auth_url = os.getenv('AUTH_URL')
        response = requests.get(f"{auth_url}/user_id/token", headers={"Authorization": auth_header})

        if response.status_code != 200:
            return jsonify({"error": "Invalid authorization"}), response.status_code

        # Extract user_id from the token response
        user_id = response.json().get('userId')
        if not user_id:
            return jsonify({"error": "User ID not found in token response"}), 400

        # Check if the user exists in the database
        user_repository = db_factory.get_user_repository()
        user = user_repository.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": f"No user found with ID {user_id}"}), 404

        # Parse and validate the input data
        data = request.get_json()
        try:
            dto = DtoRegisterPersonalData.from_json(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        # Check if a personal data entry already exists for this user
        personal_data_repository = db_factory.get_personal_data_repository()
        existing_personal_data = personal_data_repository.get_personal_data_by_user_id(user_id)
        print(existing_personal_data)
        if existing_personal_data:
            return jsonify({"error": "Personal data is already registered for this user"}), 400

        # Save the personal data
        personal_data = PersonalDataModel(
            user_id=user_id,
            birth_date=dto.birth_date,
            height=dto.height,
            weight=dto.weight,
            body_structure=dto.body_structure
        )
        with app.app_context():
            db.session.add(personal_data)
            db.session.commit()

        return jsonify({"message": "Personal data registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
