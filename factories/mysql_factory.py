from repositories.users_repository import UsersRepository


class MySQLDatabaseFactory:
    def __init__(self, db):
        self.db = db

    def get_user_repository(self):
        """Returns a concrete implementation of the UsersRepository for MySQL."""
        return UsersRepository(self.db)