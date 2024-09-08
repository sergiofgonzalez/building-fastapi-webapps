# Dizziness Tracker &mdash; a simple FastAPI web app to track diziness episodes
> Step 1: scaffolding and setting up the stage

## Starting the project

Type:

```bash
# There's something running on my windows machine in the default port
uv run -- fastapi dev app/main.py --port 5000
```

## Testing the project

## Get all

```bash
$ http get localhost:5000/episodes -v
```

## Get by id

```bash
$ http get localhost:5000/episodes/b23b9046-5cc0-4837-a89f-463bf1ce519f -v
```

## Create episode

```bash
http get localhost:5000/episodes/b23b9046-5cc0-4837-a89f-463bf1ce519f -v
```

## Delete an episode

```bash
code
```