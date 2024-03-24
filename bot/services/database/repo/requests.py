from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepo
from .topic import TopicRepo
from .user import UserRepo


class RequestsRepo(BaseRepo):
    """
    Repository for handling database operations.
    This class holds all the repositories for the database models.
    """

    _session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self._session)

    @property
    def topics(self) -> TopicRepo:
        """
        The Topic repository sessions are required to manage topic operations.
        """
        return TopicRepo(self._session)
