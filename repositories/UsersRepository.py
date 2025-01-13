from sqlalchemy import Table, MetaData, select


class UsersRepository:
    def __init__(self, db):
        self.db = db
        self.metadata = MetaData()

    def map_user_to_dict(self, result):
        """Map a user object to a dictionary."""
        with self.db.engine.connect() as connection:
            user_table = Table('user', self.metadata, autoload_with=self.db.engine)
            # Map results to dictionaries
            columns = user_table.columns.keys()
            users = [dict(zip(columns, row)) for row in result.fetchall()]
        return users

    def get_all_users(self):
        """Fetch all users from the 'user' table."""
        with self.db.engine.connect() as connection:
            user_table = Table('user', self.metadata, autoload_with=self.db.engine)
            query = select(user_table)
            results = connection.execute(query)

        return UsersRepository.map_user_to_dict(self, results)

    def get_user_by_id(self, user_id):
        """Fetch a user from the 'user' table based on the id."""
        with self.db.engine.connect() as connection:
            user_table = Table('user', self.metadata, autoload_with=self.db.engine)
            query = select(user_table).where(user_table.c.user_id == user_id)
            results = connection.execute(query)

        return UsersRepository.map_user_to_dict(self, results)