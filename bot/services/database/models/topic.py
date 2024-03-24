from sqlalchemy import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64


class Topic(Base):
    """
    SQLAlchemy model for "topics" table.

    Attributes:
    - id (Int64): Primary key, unique and non-nullable.
    - youth_policy_topic (int, optional): Optional integer column.
    - psychologist_support_topic (int, optional): Optional integer column.
    - legal_support_topic (int, optional): Optional integer column.

    Table: "topics"
    """

    __tablename__ = "topics"

    id: Mapped[Int64] = mapped_column(primary_key=True)
    youth_policy_topic: Mapped[int | None] = mapped_column(INTEGER)
    psychologist_support_topic: Mapped[int | None] = mapped_column(INTEGER)
    legal_support_topic: Mapped[int | None] = mapped_column(INTEGER)
