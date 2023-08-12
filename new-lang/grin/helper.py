#helper.py
#contains minor helper functions
def to_float(entry: str) -> float:
    """Attempts to create a float from a string. Returns the
       float if successful."""
    try:
        f = float(entry)
        return f
    except ValueError:
        pass

def to_int(entry: str) -> int:
    """Attempts to create an integer from a string. Returns the
       integer if successful."""
    try:
        i = int(entry)
        return i
    except ValueError:
        pass