import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="screenshots"
)


def create_search_text(metadata: dict) -> str:
    parts = [
        metadata.get("title", ""),
        metadata.get("summary", ""),
        metadata.get("category", ""),
        metadata.get("intent", ""),
        " ".join(metadata.get("keywords", [])),
        " ".join(metadata.get("entities", [])),
    ]

    return " ".join(
        part for part in parts
        if part
    )


def add_screenshot(
    screenshot_id: int,
    metadata: dict
):
    search_text = create_search_text(metadata)

    embedding = model.encode(
        search_text,
        normalize_embeddings=True
    ).tolist()

    collection.add(
        ids=[str(screenshot_id)],
        embeddings=[embedding],
        documents=[search_text],
        metadatas=[
            {
                "screenshot_id": screenshot_id
            }
        ]
    )


def search_screenshots(
    query: str,
    limit: int = 5
):
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

    return results