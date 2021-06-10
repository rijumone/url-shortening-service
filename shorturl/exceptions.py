"""
Module to hold Exception classes
for the shorturl package.
"""


class ShortURL404(Exception):
    """
    Exception class for errors where the short_url
    either does not exist on the database or is not a
    valid hash
    """
