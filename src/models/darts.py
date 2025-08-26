"""
darts Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting darts data.
- The Pydantic schema for validating API requests when creating a darts.

"""

from sqlalchemy import Column, DateTime, Integer, String
from framework.db import Base
from datetime import datetime, UTC
from pydantic import BaseModel
from typing import Optional


class darts(Base):
    """
    SQLAlchemy ORM model representing a darts record.

    Attributes:
        id (int): Primary key, unique identifier for the record.
        username (str): Unique username, up to 50 characters. Cannot be null.
        game (str): Required the game played, example: cricket.
        game_type (str): practice, competition.
        throws (int | None): Optional number of throws to complete the game.
        score (int | None): Optional score of the game.
        max_score (int | None): Optional maximum score with the game.
        create_date (datetime): Timestamp when the record was created (UTC).
        update_date (datetime): Timestamp when the record was last updated (UTC).

    Notes:
        - `create_date` is automatically set when the record is created.
        - `update_date` is automatically updated whenever the record changes.
    """
    __tablename__ = "darts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=False, nullable=False, index=True)
    game = Column(String(50), unique=False, nullable=False, index=True)
    game_type = Column(String(50), unique=False, nullable=False, index=False)
    throws = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    max_score = Column(Integer, nullable=True)
    create_date = Column(DateTime, default=lambda: datetime.now(UTC))
    update_date = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)  # auto-update on change
    )

    def __repr__(self):
        """
        Returns a string representation of the darts instance.

        Example:
            <darts(id=1, username='jcurtis', game='cricket')>
        """
        return f"<darts(id={self.id}, username='{self.username}', game='{self.game}')>"


class dartsCreate(BaseModel):
    """
    Pydantic schema for creating a new darts.

    Attributes:
        username (str): Required username for the new user.
        game (str): Required the game played, example: cricket.
        game_type (str): practice, competition.
        throws (int | None): Optional number of throws to complete the game.
        score (int | None): Optional score of the game.
        max_score (int | None): Optional maximum score within the game.

    Example:
        {
            "username": "johndoe",
            "game": "score training",
            "game_type": "practice",
            "throws": 10,
            "score": 56,
            "max_score": 100
        }
    """
    username: str
    game: str
    game_type: str
    throws: Optional[int] = None
    score: Optional[int] = None
    max_score: Optional[int] = None
