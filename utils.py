import uuid


def generate_uuid() -> str:
    """
    Generate a unique identifier
    """
    return str(uuid.uuid4())