from fastapi import FastAPI

app = FastAPI(
    title="MemoryLens API",
    description="AI-powered semantic screenshot search engine",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "MemoryLens API",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }