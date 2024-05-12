import re
import uuid


def generate_uuid() -> str:
    """
    Generate a unique identifier
    """
    return str(uuid.uuid4())


def remove_number(question: str) -> str:
    return re.search(f"\d+\. (.*\?)", question).group(1)
