"""Schema definitions for application API Layer."""

from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, field_validator


class DizzinessLevel(Enum):
    """Describes the level of dizziness."""

    level_0_not_dizzy = "level_0_not_dizzy"
    level_1_slightly_dizzy = "level_1_slightly_dizzy"
    level_2_dizzy = "level_2_dizzy"
    level_3_quite_dizzy = "level_3_quite_dizzy"
    level_4_very_dizzy = "level_4_very_dizzy"
    level_5_super_dizzy = "level_5_super_dizzy"


class GetSymptomSchema(BaseModel):
    """Existing Symptom Schema."""

    id: UUID
    desc: str


class CreateJournalEntrySchema(BaseModel):
    """New Journal Entry Schema."""

    day: date
    level: DizzinessLevel
    remarks: str | None = ""

    @field_validator("remarks")
    @classmethod
    def remarks_not_null(cls, value: str | None) -> str:
        """Ensure that client can't send remarks: null."""
        if value is None:
            msg = "remarks if used must not be None"
            raise AssertionError(msg)
        return value


class ReplaceJournalEntrySchema(CreateJournalEntrySchema):
    """Replaced Journal Entry Schema."""

    episode_id: UUID


class GetJournalEntrySchema(CreateJournalEntrySchema):
    """Existing Journal Entry Schema."""

    id: UUID
    symptoms: list[GetSymptomSchema]
    episode_id: UUID | None


class UpdateJournalEntrySchema(BaseModel):
    """Update of existing Journal Entry Schema."""

    day: date | None = None
    level: DizzinessLevel | None = None
    remarks: str | None = None
    episode_id: UUID | None = None


class GetJournalEntriesSchema(BaseModel):
    """List of Journal Entries Schema."""

    entries: list[GetJournalEntrySchema]


class GetEpisodeSchema(BaseModel):
    """Full representation of an episode."""

    id: UUID
    is_open: bool
    entries: list[UUID]
