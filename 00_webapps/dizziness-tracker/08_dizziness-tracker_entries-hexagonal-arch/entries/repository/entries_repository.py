"""Repository class for the Journal Entries model."""

from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from entries.repository.models import JournalEntryModel
from entries.service.entries import JournalEntry


class EntriesRepository:
    """Repository for the data access layer.

    Exposes a consistent interface to the core layer to interact with the
    database in charge of persisting the data owned by the microservice.
    """

    def __init__(self, session: Session) -> None:
        """Receives a session object representing the database session."""
        self.session = session

    def add(self, entry_dict: dict) -> JournalEntry:
        """Add a new entry to the in-memory session.

        Args:
        ----
            entry_dict: a plain dict representation of a JournalEntry.

        Returns:
        -------
            the JournalEntry object that has just been added to the session.

        """
        record = JournalEntryModel(**entry_dict)
        self.session.add(record)
        record_dict = record.dict()
        return JournalEntry(**record_dict, entry=record)

    def _get(self, entry_id: UUID) -> JournalEntryModel | None:
        return (
            self.session.query(JournalEntryModel)
            .filter(JournalEntryModel.id == str(entry_id))
            .first()
        )

    def find_by_id(self, entry_id: UUID) -> JournalEntry | None:
        """Return the JournalEntryModel object identified by the given id."""
        entry = self._get(entry_id)
        if entry is not None:
            return JournalEntry(**entry.dict())
        return None

    def find_all(
        self, limit: int | None = None, **filters: dict
    ) -> list[JournalEntry]:
        """Return all the JournalEntryModel objects."""
        query = self.session.query(JournalEntryModel)
        records = query.limit(limit).all()
        return [JournalEntry(**record.dict()) for record in records]

    def update(self, entry_id: UUID, **entry_dict: dict) -> JournalEntry | None:
        """Update the given JournalEntryModel object."""
        record = self._get(entry_id)
        if record is not None:
            for key, value in entry_dict.items():
                setattr(record, key, value)
            return JournalEntry(**record.dict())
        return None

    def delete(self, entry_id: UUID) -> None:
        """Delete the given JournalEntryModel object."""
        self.session.delete(self._get(entry_id))
