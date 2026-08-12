from fastapi import FastAPI

from api.v1 import router as v1_router
from cache.summary_cache import SummaryCache
from databases.postgres import create_postgres_db

app = FastAPI()


@app.on_event("startup")  # type: ignore[reportDeprecated]
def startup() -> None:
    """Execute the tasks on app startup."""
    create_postgres_db()
    app.state.summary_cache = SummaryCache()


app.include_router(v1_router, prefix="/api/v1")
