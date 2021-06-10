"""
Marshmallow Schemas to be used for input
validation for routes in the shorturl package.
"""

from marshmallow import Schema, fields


class EncodeInputSchema(Schema):
    """
    Validation schema for the /encode route

    Args:
        url: The original URL which needs to be encoded

    """

    url = fields.Str(required=True)


class DecodeInputSchema(Schema):
    """
    Validation schema for the /decode route

    Args:
        short_url: The short URL whose original URL needs to be looked up

    """

    short_url = fields.Str(required=True)
