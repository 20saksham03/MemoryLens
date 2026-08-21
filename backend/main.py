from fastapi import FastAPI, File, HTTPException, UploadFile

from services.gemini_service import analyze_screenshot


app = FastAPI(
    title="MemoryLens API",
    description="AI-powered semantic screenshot search engine",
    version="0.1.0",
)


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


@app.post("/api/upload")
async def upload_screenshot(file: UploadFile = File(...)):
    allowed_types = {
        "image/png",
        "image/jpeg",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPEG, and WEBP images are supported.",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    try:
        analysis = analyze_screenshot(
            image_bytes=image_bytes,
            mime_type=file.content_type,
        )

        return {
            "success": True,
            "filename": file.filename,
            "analysis": analysis,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Screenshot analysis failed: {str(exc)}",
        )