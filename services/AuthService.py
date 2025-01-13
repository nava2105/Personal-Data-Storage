import os
import requests
from flask import jsonify
from dtos.DtoPersonalData import DtoPersonalData  # Import DtoPersonalData here


class AuthService:
    """Service class to handle authentication and user data operations."""

    @staticmethod
    def authenticate_user(auth_header):
        """
        Authenticate the user and return user_id based on the authorization header.
        Raises exceptions for invalid authorization or missing user ID.
        """
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

    @staticmethod
    def get_user_and_personal_data(auth_header, request, db_factory):
        """
        Encapsulates the logic to authenticate the user, parse request data, and fetch personal data.
        
        Returns:
        - user_id: The authenticated user's ID.
        - dto: A validated DtoPersonalData object.
        - existing_personal_data: The user's personal data from the repository.
        - error_response: A Flask-style error response (None if no errors occurred).
        """
        try:
            user_id = AuthService.authenticate_user(auth_header)
            data = request.get_json()
            try:
                dto = DtoPersonalData.from_json(data)
            except ValueError as e:
                return None, None, jsonify({"error": str(e)}), 400  # Return error response if invalid
            personal_data_repository = db_factory.get_personal_data_repository()
            existing_personal_data = personal_data_repository.get_personal_data_by_user_id(user_id)
            return user_id, dto, existing_personal_data, None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None, None, None, jsonify({"error": f"An error occurred: {str(e)}"})