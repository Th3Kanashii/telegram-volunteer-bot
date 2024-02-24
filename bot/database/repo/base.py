from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    """
    A class representing a base repository for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.
    """

    def __init__(self, session) -> None:
        self.session: AsyncSession = session
