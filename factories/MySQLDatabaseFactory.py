from repositories.PersonalDataRepository import PersonalDataRepository
from repositories.UsersRepository import UsersRepository


class MySQLDatabaseFactory:
    def __init__(self, db):
        self.db = db

    def get_user_repository(self):
        """Returns a concrete implementation of the UsersRepository for MySQL."""
        return UsersRepository(self.db)

    def get_personal_data_repository(self):
        """Returns a concrete implementation of the UsersRepository for MySQL."""
        return PersonalDataRepository(self.db)