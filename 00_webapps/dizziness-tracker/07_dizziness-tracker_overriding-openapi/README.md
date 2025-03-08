# Dizziness Tracker &mdash; a simple FastAPI web app to track diziness episodes
> Step 7: wiring our own OpenAPI spec doc and tailoring the serving URLs

In this step we override the dynamically generated OpenAPI spec with our own one and also customize the URLs in which the document, and the SwaggerUI are served.

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
