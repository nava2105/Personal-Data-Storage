from flask import Flask, jsonify, request
from utils.db import db
from config.db_config import DatabaseConfig
from dotenv import load_dotenv
import requests
from factories.mysql_factory import MySQLDatabaseFactory
import os
from models.user import UserModel
from models.personal_data import PersonalDataModel

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


@app.route('/users', methods=['GET'])
def get_users():
    """Endpoint to get all users using the abstract factory."""
    user_repository = db_factory.get_user_repository()
    users = user_repository.get_all_users()
    return jsonify(users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run()
