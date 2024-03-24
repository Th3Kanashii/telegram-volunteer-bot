from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base


class BaseRepo:
    """
    A class representing a base repository for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.
    """

    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the repository with the given database session.

        :param AsyncSession session: The database session.
        """
        self._session = session

    async def commit(self, *instances: Base) -> None:
        """
        Save changes to the database.

        :param instances: Instances of Base model to be committed.
        """
        self._session.add_all(instances)
        await self._session.commit()
