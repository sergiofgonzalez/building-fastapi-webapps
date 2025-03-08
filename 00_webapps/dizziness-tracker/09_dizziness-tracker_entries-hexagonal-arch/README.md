# Dizziness Tracker &mdash; a simple FastAPI web app to track diziness episodes - v1
> Step 8.1: Redefining the project structure to accommodate the hexagonal architecture

| NOTE: |
| :---- |
| This version resumes [08_dizziness-tracker_entries-hexagonal-arch](../08_dizziness-tracker_entries-hexagonal-arch/README.md) with the new data model. |

In this step we reorganize the project to accommodate the hexagonal architecture (also called the architecture of ports and adapters) and reinforce the separation between the core, api, and data layers.

## ToDo

Next:
+ Review models from 08, include dict, and rest of the code.
+ Understand when __init__ is invoked in context managers. The engine is supposed to be created only once per app.
+ work out the filters
+ Review the alembic thingy for the migrations
+ introduce loguru
+ fix db location (parameterize it)
+ test "/entries/" and "/entries" - has it been fixed yet?
+ Can this be simplified: The assertion error was raised from the flakes layer. Now with the exceptions in place this should fail automatically, right?, right?
```
    try:
        with UnitOfWork() as unit_of_work:
            repo = EntriesRepository(unit_of_work.session)
            entries_service = EntriesService(repo)
            entry_dict = entry.model_dump()
            entries_service.add_entry(entry_dict)
    except AssertionError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
```
+ Test to create a duplicate entry

+ Document why we need to include the record object in the Order service

## Setting up shop

To set up shop:

```bash
uv init 09_dizziness-tracker_entries-hexagonal-arch
```

Then configure the ruff stuff in the `pyproject.toml`:

```toml
[tool.ruff]
# Set the maximum line length to 80
line-length = 80

[tool.ruff.lint]
# ignore = [
#   "T201",    # Allow print statements
#   "S101",    # Allow assert statements
# ]

select = ["ALL"]
```

Copy the debug launch configuration:

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "fastapi",
      "args": [
        "dev",
        "--port",
        "5000"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

Then add the FastAPI dependency:

```bash
uv add fastapi --extra standard
```

## Starting the project

Type:

```bash
# There's something running on my windows machine in the default port
uv run -- fastapi dev app/main.py --port 5000
```

## Testing the project

You can use httpie to manually test the endpoints:

```bash
$ http localhost:5000/entries limit==3 open==false
```

```bash
$ http get localhost:5000/entries/00064d59-4d77-4340-b946-b0551a7b4a50
```

```bash
$ http post localhost:5000/entries day="2024-09-07" level="level_0_not_dizzy" remarks="feeling OK"
```

```bash
http put localhost:5000/entries/8fe6b0b2-f8c3-4552-8859-6d5bf1bb211b day="2024-09-13" level=level_1_slightly_dizzy remarks="in hospital and coughing"
```

```bash
$ http patch localhost:5000/entries/996a9957-206f-4625-ad80-457abd1cb43b day="2024-09-08"
```

```bash
$ http patch localhost:5000/entries/4eb3009f-1411-46a4-b499-a6e653583ac3 episode_id="5f316e71-80b7-4cd5-a0ae-8f480014957f"
```

```bash
http delete localhost:5000/entries/00064d59-4d77-4340-b946-b0551a7b4a50
```

## Accessing Swagger docs

Point your browser to: http://localhost:5000/docs
