import json

from database.database import get_connection
from services.vector_service import add_screenshot


connection = get_connection()

rows = connection.execute(
    """
    SELECT
        id,
        title,
        summary,
        category,
        intent,
        keywords,
        entities
    FROM screenshots
    """
).fetchall()

connection.close()


for row in rows:

    metadata = {
        "title": row["title"],
        "summary": row["summary"],
        "category": row["category"],
        "intent": row["intent"],
        "keywords": json.loads(
            row["keywords"] or "[]"
        ),
        "entities": json.loads(
            row["entities"] or "[]"
        )
    }

    try:

        add_screenshot(
            row["id"],
            metadata
        )

        print(
            f"Indexed screenshot {row['id']}"
        )

    except Exception as e:

        print(
            f"Failed to index {row['id']}: {e}"
        )