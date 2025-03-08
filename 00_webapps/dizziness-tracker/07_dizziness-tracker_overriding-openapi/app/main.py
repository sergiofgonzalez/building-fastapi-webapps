"""Entry point for the web app."""

from pathlib import Path
from typing import Annotated
from uuid import UUID

import yaml
from fastapi import FastAPI, HTTPException, Query, status

from app.fakes import create, delete, find_all, find_by_id, replace, update
from app.schemas import (
    CreateJournalEntrySchema,
    GetJournalEntriesSchema,
    GetJournalEntrySchema,
    UpdateJournalEntrySchema,
)

app = FastAPI(
    openapi_url="/openapi/entries.json",  # URL where OpenAPI spec is available
    docs_url="/docs/entries",  # URL where SwaggerUI is available
)

oas_doc = yaml.safe_load((Path(__file__).parent / "../oas.yaml").read_text())

app.openapi = lambda: oas_doc


@app.get("/entries")
def list_entries(
    is_status_open: Annotated[bool | None, Query(alias="open")] = None,
    limit: Annotated[int | None, Query(ge=1)] = None,
) -> GetJournalEntriesSchema:
    """Request the retrieval of all available Journal Entries."""
    entries = find_all(is_status_open, limit)
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error


@app.delete("/entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: UUID) -> None:
    """Request the deletion of an existing entry, given its id."""
    delete(entry_id)
