import re
import uuid


def generate_uuid() -> str:
    """
    Generate a unique identifier
    """
    return str(uuid.uuid4())


def remove_number(question: str) -> str:
    """
   Remove the numbering from a question string.
   Args:
       question (str): The question string containing a numbering followed by the actual question.
   Returns:
       str: The question string with the numbering removed.
   """
    if question and question[0].isdigit():
        result = re.search(f"\d+\. (.*\?)", question)
        if result:
            return result.group(1)
