from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    @abstractmethod
    def get_user_repository(self):
        """Abstract method to return a user repository."""
        pass

    @abstractmethod
    def get_personal_data_repository(self):
        """Abstract method to return a personal data repository."""
        pass