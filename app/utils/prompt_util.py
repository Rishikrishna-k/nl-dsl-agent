import os

def load_prompt_from_file(filepath):
    """
    Load a prompt from a file and return it as a string.
    Returns None if the file does not exist.
    """
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read() 