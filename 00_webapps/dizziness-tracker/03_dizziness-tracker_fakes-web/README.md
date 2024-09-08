# Dizziness Tracker &mdash; a simple FastAPI web app to track diziness episodes
> Step 3: Adding a fake data layer accessible from the web layer.

Note that only the `/entries` routes are exposed for now. The symptoms, which are mostly a static codetable that maps the level of dizziness with a list of symptoms, and the episodes, which are computed through the journal entries. Are left for when a service layer is put into place.

## Starting the project

Type:

```bash
# There's something running on my windows machine in the default port
uv run -- fastapi dev app/main.py --port 5000
```

## Testing the project

You can use httpie to manually test the endpoints:

```bash
$ http get localhost:5000/entries/b7f3ac61-8203-4ef1-af94-cb99a8a3dd80
```

```bash
$ http post localhost:5000/entries day="2024-09-07" level="level_0_not_dizzy" remarks="feeling OK"
```

```bash
$ http patch localhost:5000/entries/15a578ef-eb80-4e4d-a0ad-b51cae802f2a day="2024-09-08"
```



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
