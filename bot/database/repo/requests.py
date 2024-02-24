from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base
from .users import UserRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations.
    This class holds all the repositories for the database models.
    """

    __session: AsyncSession

    async def commit(self, *instances: Base) -> None:
        """
        Save changes to the database.

        :param instances: Instances of Base model to be committed.
        """
        self.__session.add_all(instances)
        await self.__session.commit()

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.__session)
