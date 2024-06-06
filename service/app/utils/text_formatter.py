def camel_to_snake_formatter(text: str) -> str:
    result = "".join(["_" + c.lower() if c.isupper() else c for c in text])
    return result.lstrip("_")
