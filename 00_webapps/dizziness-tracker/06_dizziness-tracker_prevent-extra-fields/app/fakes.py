"""Fake data for the web layer."""

from datetime import date
from uuid import UUID, uuid4

from app.schemas import (
    CreateJournalEntrySchema,
    DizzinessLevel,
    GetEpisodeSchema,
    GetJournalEntrySchema,
    GetSymptomSchema,
    UpdateJournalEntrySchema,
)

_symptoms_by_level: dict[DizzinessLevel, list[GetSymptomSchema]] = {
    DizzinessLevel.level_0_not_dizzy.value: [
        GetSymptomSchema(
            id="f73b0e80-66bb-4270-b48b-4cae304cc567",
            desc="No symptoms, as before or after having an episode",
        ),
        GetSymptomSchema(
            id="c505d1cb-98d3-4fdb-9144-6bbaf1c84aca",
            desc="Fully functional",
        ),
    ],
    DizzinessLevel.level_1_slightly_dizzy.value: [
        GetSymptomSchema(
            id="1b19854f-21ee-455a-a5e5-cf85feaf2ba1",
            desc="A little light-headed",
        ),
        GetSymptomSchema(
            id="95a1a642-75b1-4430-9365-f40a5780a5c2",
            desc="Ear ringing",
        ),
        GetSymptomSchema(
            id="b09ed7d5-f332-4861-88ec-5a4cb2b88ae4",
            desc="Can work, jog, walk, and eat without issues",
        ),
        GetSymptomSchema(
            id="50f942ae-3a7f-435d-9aad-0b7375e0e45d",
            desc="Still functional.",
        ),
    ],
    DizzinessLevel.level_2_dizzy.value: [
        GetSymptomSchema(
            id="21d54b14-c242-44ad-beac-243791106c65",
            desc="Feeling uncomfortable",
        ),
        GetSymptomSchema(
            id="a8e2e662-db33-411f-9d5d-182d585263f3",
            desc="Notable ear ringing",
        ),
        GetSymptomSchema(
            id="a0c79444-cbe7-45ad-937c-084f34addbbc",
            desc="Can work, jog, eat",
        ),
        GetSymptomSchema(
            id="f2fa04e2-644f-42ff-864e-a8ddfc932e0a",
            desc="No stomach issues",
        ),
    ],
    DizzinessLevel.level_3_quite_dizzy.value: [
        GetSymptomSchema(
            id="03f11711-1e5e-42c4-be96-55b8e68fa81b",
            desc="Having problems walking, while looking down",
        ),
        GetSymptomSchema(
            id="8c2271ff-60be-4692-a9bd-94000bb95d06",
            desc="Can work but cannot focus properly on tasks",
        ),
        GetSymptomSchema(
            id="153948a6-30b4-4bce-aac9-970784793135",
            desc="Could run, but don't feel like to",
        ),
        GetSymptomSchema(
            id="e92870c4-f5d6-45d3-b1a1-93cc9abfbc14",
            desc="Bad stomach but not puking, can eat",
        ),
    ],
    DizzinessLevel.level_4_very_dizzy.value: [
        GetSymptomSchema(
            id="1a2465f3-730a-444d-ae0a-b26cc24bb7c6",
            desc="Don't feel like walking, can barely walk",
        ),
        GetSymptomSchema(
            id="e5364a7d-b698-4be4-8f25-7ae7090166b3",
            desc="Don't feel like working or running",
        ),
        GetSymptomSchema(
            id="f475aed0-6ec6-49fc-9832-8a59d1d7e972",
            desc="No appetite",
        ),
    ],
    DizzinessLevel.level_5_super_dizzy.value: [
        GetSymptomSchema(
            id="f475aed0-6ec6-49fc-9832-8a59d1d7e972",
            desc="Must be in bed or sat down",
        ),
        GetSymptomSchema(
            id="4d03b35b-dead-475a-94cc-e2ba9f142300",
            desc="Can't eat, puking",
        ),
        GetSymptomSchema(
            id="93367001-5efb-408b-b1fd-e12af066734e",
            desc="halo effect in sight",
        ),
    ],
}

_journal_entries: dict[UUID, GetJournalEntrySchema] = {
    UUID("2d1bf7e3-0f78-475d-9038-85d67bd1b152"): GetJournalEntrySchema(
        id="2d1bf7e3-0f78-475d-9038-85d67bd1b152",
        day=date(2023, 6, 30),
        level=DizzinessLevel.level_1_slightly_dizzy,
        remarks="dizzy, but functional",
        symptoms=_symptoms_by_level[
            DizzinessLevel.level_1_slightly_dizzy.value
        ],
        episode_id="05d0af2d-7b5a-4b38-bbd9-a3d8b84f58c5",
    ),
    UUID("4eb3009f-1411-46a4-b499-a6e653583ac3"): GetJournalEntrySchema(
        id="4eb3009f-1411-46a4-b499-a6e653583ac3",
        day=date(2024, 7, 1),
        level=DizzinessLevel.level_0_not_dizzy,
        remarks="yay!",
        symptoms=_symptoms_by_level[DizzinessLevel.level_0_not_dizzy.value],
        episode_id="05d0af2d-7b5a-4b38-bbd9-a3d8b84f58c5",
    ),
    UUID("2905d65b-8164-48d6-a195-77ce3581977d"): GetJournalEntrySchema(
        id="2905d65b-8164-48d6-a195-77ce3581977d",
        day=date(2024, 7, 5),
        level=DizzinessLevel.level_1_slightly_dizzy,
        remarks="sneezed yesterday",
        symptoms=_symptoms_by_level[
            DizzinessLevel.level_1_slightly_dizzy.value
        ],
        episode_id="5f316e71-80b7-4cd5-a0ae-8f480014957f",
    ),
    UUID("00064d59-4d77-4340-b946-b0551a7b4a50"): GetJournalEntrySchema(
        id="00064d59-4d77-4340-b946-b0551a7b4a50",
        day=date(2024, 7, 6),
        level=DizzinessLevel.level_2_dizzy,
        remarks="felt a bit worse today, still functional.",
        symptoms=_symptoms_by_level[DizzinessLevel.level_2_dizzy.value],
        episode_id="5f316e71-80b7-4cd5-a0ae-8f480014957f",
    ),
}

_episodes = {
    UUID("05d0af2d-7b5a-4b38-bbd9-a3d8b84f58c5"): GetEpisodeSchema(
        id="05d0af2d-7b5a-4b38-bbd9-a3d8b84f58c5",
        is_open=False,
        entries=[
            "2d1bf7e3-0f78-475d-9038-85d67bd1b152",
            "4eb3009f-1411-46a4-b499-a6e653583ac3",
        ],
    ),
    UUID("5f316e71-80b7-4cd5-a0ae-8f480014957f"): GetEpisodeSchema(
        id="5f316e71-80b7-4cd5-a0ae-8f480014957f",
        is_open=True,
        entries=[
            "2905d65b-8164-48d6-a195-77ce3581977d",
            "00064d59-4d77-4340-b946-b0551a7b4a50",
        ],
    ),
}


def find_all(
    is_status_open: bool | None = None,
    limit: int | None = None,
) -> list[GetJournalEntrySchema]:
    """Return all journal entries."""
    entries = list(_journal_entries.values())
    if is_status_open is not None:
        if is_status_open:
            entries = [
                entry
                for entry in entries
                if _episodes[entry.episode_id].is_open
            ]
        else:
            entries = [
                entry
                for entry in entries
                if not _episodes[entry.episode_id].is_open
            ]
    if limit is not None:
        return entries[-limit:]
    return entries


def find_by_id(entry_id: UUID) -> GetJournalEntrySchema:
    """Return the entry that matches the given id or None, if not found."""
    return _journal_entries.get(entry_id)


def _find_by_day(day: date) -> GetJournalEntrySchema | None:
    for entry in _journal_entries.values():
        if entry.day == day:
            return entry
    return None


def _fail_if_duplicate(day: date, entry_id: UUID | None = None) -> None:
    if (
        (found_entry := _find_by_day(day))
        and entry_id
        and found_entry.id != entry_id
    ):
        err_msg = f"day {day} would create a duplicate"
        raise AssertionError(err_msg)


def create(entry: CreateJournalEntrySchema) -> GetJournalEntrySchema:
    """Create a new entry and add it to the existing ones."""
    _fail_if_duplicate(entry.day)
    new_id = uuid4()
    new_journal_entry = GetJournalEntrySchema(
        id=new_id,
        day=entry.day,
        level=entry.level,
        remarks=entry.remarks,
        symptoms=_symptoms_by_level[entry.level.value],
        episode_id=uuid4(),  # only doing basic episode management in fake layer
    )
    _journal_entries[new_id] = new_journal_entry
    _episodes[new_journal_entry.episode_id] = GetEpisodeSchema(
        id=new_journal_entry.episode_id,
        is_open=True,
        entries=[new_journal_entry.id],
    )
    return new_journal_entry


def replace(
    entry_id: UUID,
    entry: CreateJournalEntrySchema,
) -> GetJournalEntrySchema | None:
    """Replace an existing entry by the given one."""
    _fail_if_duplicate(entry.day)
    if not (saved_entry := find_by_id(entry_id)):
        return None
    replaced_journal_entry = GetJournalEntrySchema(
        id=entry_id,
        day=entry.day,
        level=entry.level,
        remarks=entry.remarks,
        symptoms=_symptoms_by_level[entry.level.value],
        episode_id=saved_entry.episode_id,
    )
    _journal_entries[entry_id] = replaced_journal_entry
    return replaced_journal_entry


def update(
    entry_id: UUID,
    entry: UpdateJournalEntrySchema,
) -> GetJournalEntrySchema | None:
    """Update an existing entry with the information sent."""
    if entry.day:
        _fail_if_duplicate(entry.day, entry_id)
    saved_entry = find_by_id(entry_id)
    if not saved_entry:
        return None
    updated_entry = GetJournalEntrySchema(
        id=entry_id,
        day=entry.day if entry.day else saved_entry.day,
        level=entry.level if entry.level else saved_entry.level,
        remarks=entry.remarks if entry.remarks else saved_entry.remarks,
        symptoms=_symptoms_by_level[entry.level.value]
        if entry.level
        else saved_entry.symptoms,
        episode_id=entry.episode_id
        if entry.episode_id
        else saved_entry.episode_id,
    )
    _journal_entries[entry_id] = updated_entry
    if entry.episode_id and entry.episode_id != saved_entry.episode_id:
        _episodes[saved_entry.episode_id].entries.remove(entry_id)
        _episodes[entry.episode_id].entries.append(entry_id)
    return updated_entry


def delete(entry_id: UUID) -> None:
    """Delete an existing entry."""
    if entry_id in _journal_entries:
        del _journal_entries[entry_id]
