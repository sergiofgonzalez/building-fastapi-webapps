"""FastAPI web app entry point."""

from fastapi import FastAPI

from entries.web.api import entries

app = FastAPI()
app.include_router(entries.router)
