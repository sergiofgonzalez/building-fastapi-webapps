"""Model definitions for the Data Layer using SQLAlchemy."""

from datetime import UTC, date, datetime
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from entries.web.api.schemas import DizzinessLevel


def generate_uuid() -> str:
    """Generate a UUID v4 to be used for the primary key in the models."""
    return str(uuid4())


class Base(DeclarativeBase):
    """Acquiring a new Declarative Base by subclassing DeclarativeBase."""


class LevelModel(Base):
    """Represents the dizziness level in the data layer."""

    __tablename__ = "level"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_uuid,
    )
    level: Mapped[DizzinessLevel] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    symptoms: Mapped[list["SymptomModel"]] = relationship(
        back_populates="level",
    )
    entries: Mapped[list["JournalEntryModel"]] = relationship(
        back_populates="level",
    )

    def __repr__(self) -> str:
        """Developer-level string representation of LevelModel."""
        return (
            f"LevelModel(id={self.id}, level={self.level}, "
            f"description={self.description})"
        )


class SymptomModel(Base):
    """Represents a dizziness symptom in the data layer."""

    __tablename__ = "symptom"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_uuid,
    )
    description: Mapped[str] = mapped_column(nullable=False)
    level_id = mapped_column(ForeignKey("level.id"))
    level: Mapped[LevelModel] = relationship(back_populates="symptoms")

    def __repr__(self) -> str:
        """Developer-level string representation of SymptomModel."""
        return f"SymptomModel(id={self.id}, description={self.description})"


class JournalEntryModel(Base):
    """Represents a dizziness journal entry in in the data layer."""

    __tablename__ = "entry"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_uuid,
    )
    day: Mapped[date] = mapped_column(
        unique=True,
        default=datetime.now(tz=UTC).date(),
    )
    remarks: Mapped[str | None]
    level_id = mapped_column(ForeignKey("level.id"))
    level: Mapped[LevelModel] = relationship(back_populates="entries")

    def __repr__(self) -> None:
        """Developer-level representation of a JournalEntryModel."""
        return (
            f"JournalEntryModel(id={self.id}, day={self.day}, "
            f"remarks={self.remarks})"
        )
