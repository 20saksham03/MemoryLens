from services.vector_service import add_screenshot, search_screenshots


add_screenshot(
    999,
    {
        "title": "Sony Headphones",
        "summary": "Wireless noise cancelling headphones",
        "category": "Shopping",
        "intent": "Buy Later",
        "keywords": [
            "Sony",
            "headphones",
            "wireless"
        ],
        "entities": [
            "Sony WH-1000XM5"
        ]
    }
)


results = search_screenshots(
    "things I wanted to buy"
)

print(results)