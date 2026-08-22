import json
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from database.database import get_connection
from services.gemini_service import analyze_screenshot

from services.vector_service import add_screenshot

router = APIRouter(
    prefix="/api/screenshots",
    tags=["Screenshots"],
)


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


@router.post("/upload")
async def upload_screenshot(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
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

    # Generate a unique filename.
    extension = Path(file.filename or "").suffix.lower()

    if extension not in {".png", ".jpg", ".jpeg", ".webp"}:
        extension = ".png"

    unique_filename = f"{uuid.uuid4().hex}{extension}"

    image_path = UPLOAD_DIR / unique_filename

    image_path.write_bytes(image_bytes)

    try:
        analysis = analyze_screenshot(
            image_bytes=image_bytes,
            mime_type=file.content_type,
        )

        connection = get_connection()

        cursor = connection.execute(
            """
            INSERT INTO screenshots (
                filename,
                title,
                summary,
                category,
                intent,
                keywords,
                entities,
                date,
                price,
                location,
                image_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                file.filename or unique_filename,
                analysis.get("title"),
                analysis.get("summary"),
                analysis.get("category"),
                analysis.get("intent"),
                json.dumps(analysis.get("keywords", [])),
                json.dumps(analysis.get("entities", [])),
                analysis.get("date"),
                analysis.get("price"),
                analysis.get("location"),
                str(image_path),
            ),
        )

        screenshot_id = cursor.lastrowid

        connection.commit()
        add_screenshot(
            screenshot_id,
            analysis
        )
        connection.close()

        return {
            "success": True,
            "id": screenshot_id,
            "filename": file.filename,
            "image_url": f"/uploads/{unique_filename}",
            "analysis": analysis,
        }

    except Exception as exc:
        # If analysis/storage fails, remove the uploaded image.
        if image_path.exists():
            image_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Screenshot processing failed: {str(exc)}",
        )

    
@router.get("")
def get_screenshots():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            filename,
            title,
            summary,
            category,
            intent,
            keywords,
            entities,
            date,
            price,
            location,
            image_path,
            created_at
        FROM screenshots
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    screenshots = []

    for row in rows:
        screenshots.append(
            {
                "id": row["id"],
                "filename": row["filename"],
                "title": row["title"],
                "summary": row["summary"],
                "category": row["category"],
                "intent": row["intent"],
                "keywords": json.loads(row["keywords"] or "[]"),
                "entities": json.loads(row["entities"] or "[]"),
                "date": row["date"],
                "price": row["price"],
                "location": row["location"],
                "image_url": f"/uploads/{Path(row['image_path']).name}",
                "created_at": row["created_at"],
            }
        )

    return {
        "screenshots": screenshots,
        "count": len(screenshots),
    }