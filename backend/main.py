from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.database import initialize_database
from routes.screenshots import router as screenshots_router

from routes.search import router as search_router

app = FastAPI(
    title="MemoryLens API",
    description="AI-powered semantic screenshot search engine",
    version="0.1.0",
)


initialize_database()


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


app.include_router(screenshots_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "MemoryLens API",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }