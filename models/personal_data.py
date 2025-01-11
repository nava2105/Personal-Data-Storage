from sqlalchemy import Column,BigInteger, Double, Integer, String, ForeignKey
from utils.db import db


class PersonalDataModel(db.Model):
    __tablename__ = 'personal_data'

    personal_data_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    height = Column(Double, nullable=False)
    weight = Column(Double, nullable=False)
    body_structure = Column(String(255), nullable=False)

    def __init__(self, user_id, age, height, weight, body_structure):
        self.user_id = user_id
        self.age = age
        self.height = height
        self.weight = weight
        self.body_structure = body_structure

    def to_dict(self):
        """Converts the PersonalData object to a dictionary."""
        return {
            "personal_data_id": self.personal_data_id,
            "user_id": self.user_id,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "body_structure": self.body_structure,
        }
