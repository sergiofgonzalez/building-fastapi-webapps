# Dizziness Tracker &mdash; a simple FastAPI web app to track diziness episodes
> Step 2: Adding schemas for the API layer


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
$ http post localhost:5000/episodes entries[0][day]="2024-06-29" entries[0][level]=0_no-dizziness -v
```

## Delete an episode

```bash
code
```

## Close episode

```bash
http post localhost:5000/episodes/b23b9046-5cc0-4837-a89f-463bf1ce519f/close
```

## Reopen episode

```bash

http post localhost:5000/episodes/b23b9046-5cc0-4837-a89f-463bf1ce519f/reopen
```

## Replacing an episode (PUT)

```bash
$ http put localhost:5000/episodes/b23b9046-5cc0-4837-a89f-463bf1ce519f entries[0][day]="2024-06-29" entries[0][level]=0_no-dizziness -v
```

## Accessing Swagger docs

Point your browser to: http://localhost:5000/docs
