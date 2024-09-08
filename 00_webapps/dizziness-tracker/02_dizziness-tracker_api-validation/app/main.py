"""Dizziness Tracker - entry point for the web app."""

from datetime import UTC, date, datetime
from uuid import UUID

from fastapi import FastAPI, status

from app.schemas import CreateEpisodeSchema, GetEpisodeSchema, GetEpisodesSchema

app = FastAPI()

_episode = {
    "id": "b23b9046-5cc0-4837-a89f-463bf1ce519f",
    "status": "open",
    "created": datetime.now(UTC),
    "entries": [
        {
            "day": date(2024, 6, 29),
            "level": "1_slightly-dizzy",
            "remarks": "A bit of ear ringing; took 3x Dizinell; very sleepy",
        },
        {
            "day": date(2024, 6, 30),
            "level": "1_slightly-dizzy",
            "remarks": "Took pills morning and lunch. I could have gone jogging.",
        },
        {"day": date(2024, 7, 1), "level": "0_no-dizziness", "remarks": "yay!"},
    ],
}


@app.get("/episodes")
def list_episodes() -> GetEpisodesSchema:
    """Return the existing episodes."""
    return {"episodes": [_episode]}


@app.post("/episodes", status_code=status.HTTP_201_CREATED)
def create_episode(episode_details: CreateEpisodeSchema) -> GetEpisodeSchema:
    """Create a new episode."""
    return _episode


@app.get("/episodes/{episode_id}")
def read_episode(episode_id: UUID) -> GetEpisodeSchema:
    """Return the episode identified by the given ID."""
    return _episode


@app.post("/episodes/{episode_id}/close")
def close_episode(episode_id: UUID) -> GetEpisodeSchema:
    """Close the episode identified by the given ID."""
    return _episode


@app.post("/episodes/{episode_id}/reopen")
def reopen_episode(episode_id: UUID) -> GetEpisodeSchema:
    """Reopen the episode identified by the given ID."""
    return _episode


@app.put("/episodes/{episode_id}")
def replace_episode(episode_id: UUID, episode_details: CreateEpisodeSchema) -> GetEpisodeSchema:
    """Update an existing episode."""
    return _episode


@app.patch("/episodes/{episode_id}")
def update_episode(episode_id: UUID, episode_dict: dict) -> GetEpisodeSchema:
    """Update an existing episode."""
    return _episode


@app.delete("/episodes/{episode_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_episode(episode_id: UUID) -> None:
    """Delete the episode identified by the given ID."""
