"""Classes that represents the domain objects of the entries service.

These are the objects that manage the data of the Journal Entries and that are returned by the Journal Entries repository.
"""

from datetime import date
from uuid import UUID

from entries.repository.models import JournalEntryModel
from entries.web.api.schemas import DizzinessLevel


class JournalEntry:
    """Represents a JournalEntry."""

    def __init__(
        self,
        entry_id: UUID,
        day: date,
        level: DizzinessLevel,
        remarks: str | None = None,
        episode_id: UUID | None = None,
        entry: JournalEntryModel = None,
    ) -> None:
        """Initialize a JournalEntry object."""
        self._id = entry_id
        self.day = day
        self.level = level
        self.remarks = remarks
        self.episode_id = episode_id
        self.entry = entry

    @property
    def id(self) -> UUID:
        """Return the ID of the entry."""
        return self._id or self.entry.id

    def dict(self) -> dict:
        """Return a plain dict representation of the object."""
        return {
            "id": self.id,
            "day": self.day,
            "level": self.level,
            "remarks": self.remarks,
            "episode_id": self.episode_id,
        }
