"""Model definitions for the Data Layer using SQLAlchemy."""

import datetime
import uuid

from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKey,
    String,
    create_engine,
    insert,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from entries.web.api.schemas import DizzinessLevel

Base = declarative_base()


def generate_uuid() -> str:
    """Return a UUID value as a string."""
    return str(uuid.uuid4())


class JournalEntryModel(Base):
    """Represents a Journal Entry in the Data layer."""

    __tablename__ = "entry"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    day: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(tz=datetime.UTC).date(),
    )
    level: Mapped[DizzinessLevel] = mapped_column(nullable=False)
    remarks: Mapped[str | None]
    episode_id: Mapped[str | None]

    # I still don't know how to map this
    symptoms = Mapped[list["SymptomModel"]] = relationship(back_populates="")

    def dict(self) -> dict:
        """Return a plain dict representation of the model."""
        return {
            "entry_id": self.id,
            "day": self.day,
            "level": self.level,
            "remarks": self.remarks,
            "episode_id": self.episode_id,
        }


class SymptomModel(Base):
    """Represents a Symptom in the Data layer."""

    __tablename__ = "symptom"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    desc: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[DizzinessLevel] = mapped_column(nullable=False)

    def dict(self) -> dict:
        """Return a plain dict representation of the model."""
        return {
            "id": self.id,
            "desc": self.desc,
            "level": self.level,
        }

    def __repr__(self) -> str:
        """Developer friendly representation of the instance."""
        return (
            f"SymptomModel(id={self.id}, desc={self.desc}, level={self.level})"
        )


def _create_tables() -> None:
    # engine is supposed to be created only once per particular db and held
    # globally for the lifetime of a single app process.
    engine = create_engine("sqlite:///entries.db", echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    symptom_table = SymptomModel.__table__
    entry_table = JournalEntryModel.__table__
    with engine.connect() as conn:
        result = conn.execute(
            insert(symptom_table),
            [
                {
                    "level": DizzinessLevel.level_0_not_dizzy,
                    "desc": "No symptoms, as before or after having an episode",
                },
                {
                    "level": DizzinessLevel.level_0_not_dizzy,
                    "desc": "Fully functional",
                },
                {
                    "level": DizzinessLevel.level_1_slightly_dizzy,
                    "desc": "A little light-headed",
                },
                {
                    "level": DizzinessLevel.level_1_slightly_dizzy,
                    "desc": "Ear ringing",
                },
                {
                    "level": DizzinessLevel.level_1_slightly_dizzy,
                    "desc": "Can work, jog, walk, and eat without issues",
                },
                {
                    "level": DizzinessLevel.level_1_slightly_dizzy,
                    "desc": "Still functional",
                },
                {
                    "level": DizzinessLevel.level_2_dizzy,
                    "desc": "Feeling uncomfortable",
                },
                {
                    "level": DizzinessLevel.level_2_dizzy,
                    "desc": "Notable ear ringing",
                },
                {
                    "level": DizzinessLevel.level_2_dizzy,
                    "desc": "Can work, jog, eat",
                },
                {
                    "level": DizzinessLevel.level_2_dizzy,
                    "desc": "No stomach issues",
                },
                {
                    "level": DizzinessLevel.level_3_quite_dizzy,
                    "desc": "Having problems walking, while looking down",
                },
                {
                    "level": DizzinessLevel.level_3_quite_dizzy,
                    "desc": "Can work but cannot focus properly on tasks",
                },
                {
                    "level": DizzinessLevel.level_3_quite_dizzy,
                    "desc": "Could run, but don't feel like to",
                },
                {
                    "level": DizzinessLevel.level_3_quite_dizzy,
                    "desc": "Bad stomach but not puking, can eat",
                },
                {
                    "level": DizzinessLevel.level_4_very_dizzy,
                    "desc": "Don't feel like walking, can barely walk",
                },
                {
                    "level": DizzinessLevel.level_4_very_dizzy,
                    "desc": "Don't feel like working or running",
                },
                {
                    "level": DizzinessLevel.level_4_very_dizzy,
                    "desc": "No appetite",
                },
                {
                    "level": DizzinessLevel.level_5_super_dizzy,
                    "desc": "Must be in bed or sat down",
                },
                {
                    "level": DizzinessLevel.level_5_super_dizzy,
                    "desc": "Can't eat, puking",
                },
                {
                    "level": DizzinessLevel.level_5_super_dizzy,
                    "desc": "Halo effect in sight",
                },
            ],
        )
        conn.commit()

        with Session(engine) as session:
            symptoms = session.scalars(
                select(SymptomModel).where(
                    SymptomModel.level == DizzinessLevel.level_0_not_dizzy
                )
            ).all()
            for symptom in symptoms:
                print(symptom)

    engine.dispose()  # I only wanted to use it for the table creation


_create_tables()
