from sqlalchemy import Table, MetaData, select


class PersonalDataRepository:
    def __init__(self, db):
        self.db = db
        self.metadata = MetaData()

    def map_personal_data_to_dict(self, result):
        """Map a user's personal data object to a dictionary."""
        with self.db.engine.connect() as connection:
            personal_data_table = Table('personal_data', self.metadata, autoload_with=self.db.engine)
            # Map results to dictionaries
            columns = personal_data_table.columns.keys()
            personal_data = [dict(zip(columns, row)) for row in result.fetchall()]
        return personal_data

    def get_all_personal_data(self):
        """Fetch all user's personal data from the 'user' table."""
        with self.db.engine.connect() as connection:
            personal_data_table = Table('personal_data', self.metadata, autoload_with=self.db.engine)
            query = select(personal_data_table)
            results = connection.execute(query)

        return PersonalDataRepository.map_personal_data_to_dict(self, results)

    def get_personal_data_by_user_id(self, user_id):
        """Fetch a user's personal data from the 'personal_data' table based on the id."""
        with self.db.engine.connect() as connection:
            personal_data_table = Table('personal_data', self.metadata, autoload_with=self.db.engine)
            query = select(personal_data_table).where(personal_data_table.c.user_id == user_id)
            results = connection.execute(query)

        return PersonalDataRepository.map_personal_data_to_dict(self, results)