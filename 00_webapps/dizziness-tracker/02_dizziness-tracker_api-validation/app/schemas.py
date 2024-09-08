"""Schema definitions in the API Layer."""

from datetime import date, datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from annotated_types import Len
from pydantic import BaseModel, Field


class DizzinessLevel(Enum):
    """Describes the level of dizziness."""

    no_dizziness_0 = "0_no-dizziness"
    slightly_dizzy_1 = "1_slightly-dizzy"
    dizzy_2 = "2_dizzy"
    quite_dizzy_3 = "3_quite-dizzy"
    very_dizzy_4 = "4_very-dizzy"
    super_dizzy_5 = "5_super-dizzy"


class Status(Enum):
    """Describes the status of the episode."""

    open = "open"
    closed = "closed"


class EpisodeEntrySchema(BaseModel):
    """Schema for each of the entries in a dizziness episode."""

    day: date
    level: DizzinessLevel
    remarks: str | None = Field(default=None)


class CreateEpisodeSchema(BaseModel):
    """Schema for the create episode payload."""

    entries: Annotated[list[EpisodeEntrySchema], Len(min_length=1)]


class GetEpisodeSchema(CreateEpisodeSchema):
    """Schema for the get episode payload."""

    id: UUID
    created: datetime
    status: Status


class GetEpisodesSchema(BaseModel):
    """Schema for the get episodes payload."""

    episodes: list[GetEpisodeSchema]
