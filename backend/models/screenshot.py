from typing import Optional

from pydantic import BaseModel


class ScreenshotResponse(BaseModel):
    id: int
    filename: str
    title: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    intent: Optional[str] = None
    keywords: list[str] = []
    entities: list[str] = []
    date: Optional[str] = None
    price: Optional[str] = None
    location: Optional[str] = None
    image_url: str