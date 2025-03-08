"""Journal Entries API layer."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from entries.repository.entries_repository import EntriesRepository
from entries.repository.unit_of_work import UnitOfWork
from entries.service.entries_service import EntriesService
from entries.web.api.schemas import (
    CreateJournalEntrySchema,
    GetJournalEntriesSchema,
    GetJournalEntrySchema,
)

router = APIRouter(prefix="/entries")


@router.get("")
@router.get("/")
def list_entries(
    is_status_open: Annotated[bool | None, Query(alias="open")] = None,
    limit: Annotated[int | None, Query(ge=1)] = None,
) -> GetJournalEntriesSchema:
    """Request the retrieval of all available Journal Entries."""
    with UnitOfWork() as unit_of_work:
        repo = EntriesRepository(unit_of_work.session)
        entries_service = EntriesService(repo)
        entries = entries_service.list_entries(
            is_status_open=is_status_open,
            limit=limit,
        )
        return {"entries": entries}

@router.post("")
@router.post("/")
def create_entry(entry: CreateJournalEntrySchema) -> GetJournalEntrySchema:
    """Request the creation of a new Journal Entry."""
    try:
        with UnitOfWork() as unit_of_work:
            repo = EntriesRepository(unit_of_work.session)
            entries_service = EntriesService(repo)
            entry_dict = entry.model_dump()
            added_entry = entries_service.add_entry(entry_dict)
            unit_of_work.commit()
            return added_entry.dict()
    except AssertionError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
