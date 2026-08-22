from turtle import distance

from fastapi import APIRouter
from pydantic import BaseModel

from services.vector_service import search_screenshots
from database.database import get_connection


router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@router.post("")
def search(request: SearchRequest):

    results = search_screenshots(
        request.query,
        request.limit
    )

    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not ids:
        return {
            "query": request.query,
            "results": []
        }

    connection = get_connection()

    placeholders = ",".join(
        "?" for _ in ids
    )

    rows = connection.execute(
        f"""
        SELECT
            id,
            filename,
            title,
            summary,
            category,
            intent,
            image_path
        FROM screenshots
        WHERE id IN ({placeholders})
        """,
        [int(i) for i in ids]
    ).fetchall()

    connection.close()

    lookup = {
        row["id"]: row
        for row in rows
    }

    output = []

    for screenshot_id, distance in zip(
        ids,
        distances
   ):

        # Chroma returns cosine distance.
        # Lower distance = more relevant.
        

        score = 1 - distance

        row = lookup.get(
            int(screenshot_id)
        )

        if not row:
            continue

        

        output.append(
            {
                "id": row["id"],
                "title": row["title"],
                "summary": row["summary"],
                "category": row["category"],
                "intent": row["intent"],
                "image_url": (
                "/uploads/"
                + row["image_path"].split("\\")[-1]
                )
            }
        )

    return {
        "query": request.query,
        "results": output
    }