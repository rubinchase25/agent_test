"""
list_utils.py

Provides list manipulation helper functions.
"""


def flatten(xs):
    """Flatten a list of lists into a single list."""
    return [item for sublist in xs for item in sublist]


def dedupe(xs):
    """Return a new list with duplicate values removed, preserving order."""
    seen = set()
    result = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
