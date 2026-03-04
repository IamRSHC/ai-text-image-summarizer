import re


def clean_text(text: str) -> str:
    """
    Cleans user input text before summarization
    """

    if not text:
        return ""

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove weird characters
    text = re.sub(r"[^\w\s\.,!?-]", "", text)

    # strip
    text = text.strip()

    return text


def is_garbage_input(text: str) -> bool:
    """
    Detect useless inputs like:
    AI AI AI AI AI
    test test test test
    aaaaaa
    """

    words = text.split()

    # too short
    if len(words) < 15:
        return True

    # repetition detection
    unique_ratio = len(set(words)) / len(words)

    if unique_ratio < 0.3:
        return True

    return False