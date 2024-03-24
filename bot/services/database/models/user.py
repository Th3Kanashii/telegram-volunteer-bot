from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from bot.enums import Locale

from .base import Base, Int64


class User(Base):
    """
    SQLAlchemy model for "users" table.

    Attributes:
    - id (Int64): Primary key, unique and non-nullable.
    - name (str): String column.
    - locale (str): String column (length: 2), default UK.
    - youth_policy (bool): Boolean column with default value False.
    - psychologist_support (bool): Boolean column with default value False.
    - civic_education (bool): Boolean column with default value False.
    - legal_support (bool): Boolean column with default value False.
    - active_category (str, optional): Optional string column (max length: 20)

    Table: "users"
    """

    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True)
    name: Mapped[str]
    locale: Mapped[str] = mapped_column(String(length=2), default=Locale.DEFAULT)
    youth_policy: Mapped[bool] = mapped_column(default=False)
    psychologist_support: Mapped[bool] = mapped_column(default=False)
    civic_education: Mapped[bool] = mapped_column(default=False)
    legal_support: Mapped[bool] = mapped_column(default=False)
    active_category: Mapped[str | None] = mapped_column(String(length=20), default=None)
