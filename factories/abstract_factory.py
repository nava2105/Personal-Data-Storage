from abc import ABC, abstractmethod


class DatabaseFactory(ABC):
    @abstractmethod
    def get_user_repository(self):
        """Abstract method to return a user repository."""
        pass