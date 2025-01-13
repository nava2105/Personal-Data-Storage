from sqlalchemy import Column,BigInteger, Double, Integer, String, Date, ForeignKey
from utils.Database import db


class PersonalDataModel(db.Model):
    __tablename__ = 'personal_data'

    personal_data_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    height = Column(Double, nullable=False)
    weight = Column(Double, nullable=False)
    body_structure = Column(String(255), nullable=False)

    def __init__(self, user_id, birth_date, height, weight, body_structure):
        self.user_id = user_id
        self.birth_date = birth_date
        self.height = height
        self.weight = weight
        self.body_structure = body_structure

    def to_dict(self):
        """Converts the PersonalData object to a dictionary."""
        return {
            "personal_data_id": self.personal_data_id,
            "user_id": self.user_id,
            "birth_date": self.birth_date,
            "height": self.height,
            "weight": self.weight,
            "body_structure": self.body_structure,
        }
