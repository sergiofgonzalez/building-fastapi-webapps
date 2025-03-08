"""Core layer of the Entries application."""

from entries.repository.entries_repository import EntriesRepository
from entries.service.entries import JournalEntry


class EntriesService:
    """Encapsulates the capabilities of the Entries domain.

    Takes care of orchestrating the Entries Repository to manage all the
    persistence activities related to entry objects and performs all the
    necessary actions on them.
    """

    def __init__(self, entries_repository: EntriesRepository) -> None:
        """Initialize an EntriesService instance by wiring the repository."""
        self.entries_repository = entries_repository

    def list_entries(self, **filters: dict) -> list[JournalEntry]:
        """Return the list of entries satisfying the given filters."""
        limit = filters.pop("limit", None)
        return self.entries_repository.find_all(limit, **filters)

    def add_entry(self, entry_dict: dict) -> JournalEntry:
        """Add a new entry."""
        # No episode management for now
        return self.entries_repository.add(entry_dict)
