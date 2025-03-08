"""Model definitions for the Data Layer using SQLAlchemy (v2)."""

import datetime
import uuid
from enum import Enum

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    String,
    Table,
    create_engine,
    insert,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


class DizzinessLevel(Enum):
    """Describes the level of dizziness."""

    level_0_not_dizzy = "level_0_not_dizzy"
    level_1_slightly_dizzy = "level_1_slightly_dizzy"
    level_2_dizzy = "level_2_dizzy"
    level_3_quite_dizzy = "level_3_quite_dizzy"
    level_4_very_dizzy = "level_4_very_dizzy"
    level_5_super_dizzy = "level_5_super_dizzy"


class Base(DeclarativeBase):
    """Acquiring a new Declarative Base by subclassing DeclarativeBase."""


def generate_uuid() -> str:
    """Return a UUID value as a string."""
    return str(uuid.uuid4())


link_table = Table(
    "entry_symptom_link",
    Base.metadata,
    Column("entry_id", ForeignKey("entry.id"), primary_key=True),
    Column("symptom_id", ForeignKey("symptom.id"), primary_key=True),
)


class JournalEntry(Base):
    """Represents a Journal Entry in the data layer."""

    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    remarks: Mapped[str | None]
    level: Mapped[DizzinessLevel] = mapped_column(nullable=False)
    symptoms: Mapped[list["Symptom"]] = relationship(
        secondary=link_table,
        secondaryjoin="JournalEntry.level == Symptom.level",
        back_populates="entries",
    )

    def __repr__(self) -> str:
        """Dev level representation of JournalEntry."""
        return (
            f"JournalEntry(id={self.id}, remarks={self.remarks}, "
            f"level={self.level})"
        )


class Symptom(Base):
    """Represent a Symptom in the data layer."""

    __tablename__ = "symptom"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[DizzinessLevel] = mapped_column(nullable=False)
    desc: Mapped[str] = mapped_column(nullable=False)
    # entries: Mapped[list[JournalEntry]] = relationship(
    #     secondary=link_table,
    #     back_populates="symptoms",
    # )

    def __repr__(self) -> str:
        """Dev level representation of a Symptom."""
        return f"Symptom(id={self.id}, level={self.level}, desc={self.desc})"


if __name__ == "__main__":
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj = Base.metadata
    metadata_obj.create_all(engine)

    # adding objects
    with Session(engine) as session:
        session.add(
            Symptom(
                level=DizzinessLevel.level_0_not_dizzy,
                desc="No symptoms, as before or after having an episode",
            ),
        )
        session.add(
            Symptom(
                level=DizzinessLevel.level_0_not_dizzy,
                desc="Fully functional",
            ),
        )
        session.add(
            Symptom(
                level=DizzinessLevel.level_1_slightly_dizzy,
                desc="A little light-headed",
            ),
        )
        session.add(
            Symptom(
                level=DizzinessLevel.level_1_slightly_dizzy,
                desc="Ear ringing",
            ),
        )

        level0_symptons = session.scalars(
            select(Symptom).where(
                Symptom.level == DizzinessLevel.level_0_not_dizzy
            ),
        ).all()

        session.add(
            JournalEntry(
                remarks="A dummy record for level 0",
                level=DizzinessLevel.level_0_not_dizzy,
            ),
        )

        session.add(
            JournalEntry(
                remarks="A dummy record for level 1",
                level=DizzinessLevel.level_1_slightly_dizzy,
            ),
        )
        session.commit()

    # selecting all entries
    with Session(engine) as session:
        stmt = select(JournalEntry)
        for row in session.execute(stmt):
            print(f"row={row}")

    # selecting a particular entry and navigating to the symptoms
    with Session(engine) as session:
        stmt = select(JournalEntry).where(JournalEntry.id == 1)
        entry1 = session.scalars(stmt).first()
        print(f"{entry1=}")
        print(f"symptoms={entry1.symptoms}")

    # selecting a particular symptom and checking the entries is not a good use
    # case though: it should be based on the level, not on the particular symptom
    with Session(engine) as session:
        stmt = select(Symptom).where(
            Symptom.level == DizzinessLevel.level_0_not_dizzy,
        )
        symptom1 = session.scalars(stmt).first()
        print(f"{symptom1=}")
        print(f"entries={symptom1.entries}")

    print("-- done!")

# class JournalEntryModel(Base):
#     """Represents a Journal Entry in the Data layer."""

#     __tablename__ = "entry"

#     id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
#     day: Mapped[datetime.datetime] = mapped_column(
#         default=datetime.datetime.now(tz=datetime.UTC).date(),
#     )
#     level: Mapped[DizzinessLevel] = mapped_column(nullable=False)
#     remarks: Mapped[str | None]
#     episode_id: Mapped[str | None]

#     # I still don't know how to map this
#     symptoms = Mapped[list["SymptomModel"]] = relationship(back_populates="")

#     def dict(self) -> dict:
#         """Return a plain dict representation of the model."""
#         return {
#             "entry_id": self.id,
#             "day": self.day,
#             "level": self.level,
#             "remarks": self.remarks,
#             "episode_id": self.episode_id,
#         }


# class SymptomModel(Base):
#     """Represents a Symptom in the Data layer."""

#     __tablename__ = "symptom"

#     id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
#     desc: Mapped[str] = mapped_column(nullable=False)
#     level: Mapped[DizzinessLevel] = mapped_column(nullable=False)

#     def dict(self) -> dict:
#         """Return a plain dict representation of the model."""
#         return {
#             "id": self.id,
#             "desc": self.desc,
#             "level": self.level,
#         }

#     def __repr__(self) -> str:
#         """Developer friendly representation of the instance."""
#         return (
#             f"SymptomModel(id={self.id}, desc={self.desc}, level={self.level})"
#         )


# def _create_tables() -> None:
#     # engine is supposed to be created only once per particular db and held
#     # globally for the lifetime of a single app process.
#     engine = create_engine("sqlite:///entries.db", echo=True)
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#     symptom_table = SymptomModel.__table__
#     entry_table = JournalEntryModel.__table__
#     with engine.connect() as conn:
#         result = conn.execute(
#             insert(symptom_table),
#             [
#                 {
#                     "level": DizzinessLevel.level_0_not_dizzy,
#                     "desc": "No symptoms, as before or after having an episode",
#                 },
#                 {
#                     "level": DizzinessLevel.level_0_not_dizzy,
#                     "desc": "Fully functional",
#                 },
#                 {
#                     "level": DizzinessLevel.level_1_slightly_dizzy,
#                     "desc": "A little light-headed",
#                 },
#                 {
#                     "level": DizzinessLevel.level_1_slightly_dizzy,
#                     "desc": "Ear ringing",
#                 },
#                 {
#                     "level": DizzinessLevel.level_1_slightly_dizzy,
#                     "desc": "Can work, jog, walk, and eat without issues",
#                 },
#                 {
#                     "level": DizzinessLevel.level_1_slightly_dizzy,
#                     "desc": "Still functional",
#                 },
#                 {
#                     "level": DizzinessLevel.level_2_dizzy,
#                     "desc": "Feeling uncomfortable",
#                 },
#                 {
#                     "level": DizzinessLevel.level_2_dizzy,
#                     "desc": "Notable ear ringing",
#                 },
#                 {
#                     "level": DizzinessLevel.level_2_dizzy,
#                     "desc": "Can work, jog, eat",
#                 },
#                 {
#                     "level": DizzinessLevel.level_2_dizzy,
#                     "desc": "No stomach issues",
#                 },
#                 {
#                     "level": DizzinessLevel.level_3_quite_dizzy,
#                     "desc": "Having problems walking, while looking down",
#                 },
#                 {
#                     "level": DizzinessLevel.level_3_quite_dizzy,
#                     "desc": "Can work but cannot focus properly on tasks",
#                 },
#                 {
#                     "level": DizzinessLevel.level_3_quite_dizzy,
#                     "desc": "Could run, but don't feel like to",
#                 },
#                 {
#                     "level": DizzinessLevel.level_3_quite_dizzy,
#                     "desc": "Bad stomach but not puking, can eat",
#                 },
#                 {
#                     "level": DizzinessLevel.level_4_very_dizzy,
#                     "desc": "Don't feel like walking, can barely walk",
#                 },
#                 {
#                     "level": DizzinessLevel.level_4_very_dizzy,
#                     "desc": "Don't feel like working or running",
#                 },
#                 {
#                     "level": DizzinessLevel.level_4_very_dizzy,
#                     "desc": "No appetite",
#                 },
#                 {
#                     "level": DizzinessLevel.level_5_super_dizzy,
#                     "desc": "Must be in bed or sat down",
#                 },
#                 {
#                     "level": DizzinessLevel.level_5_super_dizzy,
#                     "desc": "Can't eat, puking",
#                 },
#                 {
#                     "level": DizzinessLevel.level_5_super_dizzy,
#                     "desc": "Halo effect in sight",
#                 },
#             ],
#         )
#         conn.commit()

#         with Session(engine) as session:
#             symptoms = session.scalars(
#                 select(SymptomModel).where(
#                     SymptomModel.level == DizzinessLevel.level_0_not_dizzy
#                 )
#             ).all()
#             for symptom in symptoms:
#                 print(symptom)

#     engine.dispose()  # I only wanted to use it for the table creation


# _create_tables()
