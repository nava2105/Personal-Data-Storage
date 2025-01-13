from datetime import datetime

class DtoRegisterPersonalData:
    def __init__(self, birth_date, height, weight, body_structure):
        self.birth_date = birth_date
        self.height = height
        self.weight = weight
        self.body_structure = body_structure

    @staticmethod
    def from_json(json_data):
        """Validates and initializes the DTO from JSON input."""
        try:
            birth_date_string = json_data.get('birth_date')
            height = float(json_data.get('height'))
            weight = float(json_data.get('weight'))
            body_structure = str(json_data.get('body_structure'))

            try:
                birth_date = datetime.strptime(birth_date_string, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format. Expected format is YYYY-MM-DD.")
            if not body_structure:
                raise ValueError("body_structure is required")

            return DtoRegisterPersonalData(birth_date, height, weight, body_structure)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid personal data: {e}")