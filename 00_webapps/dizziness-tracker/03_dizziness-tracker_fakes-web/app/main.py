"""Entry point for the web app."""

from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from app.fakes import create, delete, find_all, find_by_id, replace, update
from app.schemas import (
    CreateJournalEntrySchema,
    GetJournalEntriesSchema,
    GetJournalEntrySchema,
    UpdateJournalEntrySchema,
)

app = FastAPI()


@app.get("/entries")
def list_entries() -> GetJournalEntriesSchema:
    """Request the retrieval of all available Journal Entries."""
    entries = find_all()
    return {"entries": entries}


@app.get("/entries/{entry_id}")
def get_entry_by_id(entry_id: UUID) -> GetJournalEntrySchema:
    """Request the retrieval of the entry identified by the given entry_id."""
    found_entry = find_by_id(entry_id)
    if found_entry:
        return found_entry
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"entry {entry_id} not found",
    )


@app.post("/entries", status_code=status.HTTP_201_CREATED)
def create_entry(entry: CreateJournalEntrySchema) -> GetJournalEntrySchema:
    """Request the creation of a new Journal Entry."""
    try:
        return create(entry)
    except AssertionError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        ) from error


@app.put("/entries/{entry_id}")
def replace_entry(
    entry_id: UUID,
    entry: CreateJournalEntrySchema,
) -> GetJournalEntrySchema:
    """Request the replacement of an existing entry by the given one."""
    try:
        replaced_entry = replace(entry_id, entry)
        if replaced_entry:
            return replaced_entry
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"entry {entry_id} not found",
        )
    except AssertionError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        ) from error


@app.patch("/entries/{entry_id}")
def update_entry(
    entry_id: UUID,
    entry: UpdateJournalEntrySchema,
) -> GetJournalEntrySchema:
    """Request the update of an existing entry by the given one."""
    try:
        updated_entry = update(entry_id, entry)
        if updated_entry:
            return updated_entry
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"entry {entry_id} not found",
        )
    except AssertionError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
        ) from error


@app.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: UUID) -> None:
    """Request the deletion of an existing entry, given its id."""
    delete(entry_id)
