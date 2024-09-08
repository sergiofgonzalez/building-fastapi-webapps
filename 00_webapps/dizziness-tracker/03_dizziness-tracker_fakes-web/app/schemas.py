"""Schema definitions for application API Layer."""

from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, validator


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
    remarks: str | None = Field(default="")

    @field_validator("remarks")
    @classmethod
    def remarks_not_null(cls, value: str | None) -> str:
        """Ensure that client can't send remarks: null."""
        if value is None:
            msg = "remarks if used must not be None"
            raise AssertionError(msg)
        return value


class GetJournalEntrySchema(CreateJournalEntrySchema):
    """Existing Journal Entry Schema."""

    id: UUID
    symptoms: list[GetSymptomSchema]


class UpdateJournalEntrySchema(BaseModel):
    """Update of existing Journal Entry Schema."""

    day: date | None = Field(default=None)
    level: DizzinessLevel | None = Field(default=None)
    remarks: str | None = Field(default=None)


class GetJournalEntriesSchema(BaseModel):
    """List of Journal Entries Schema."""

    entries: list[GetJournalEntrySchema]
