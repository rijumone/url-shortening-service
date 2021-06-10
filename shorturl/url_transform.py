
"""
Module to encode and decode URLs to short URLs
and vice versa and functionality for database
persistence.
"""
import short_url
from loguru import logger

from shorturl.models import URLsMap
from shorturl.db import get_db_session
from shorturl.exceptions import ShortURL404


class ShortURL:
    """
    Class to generate a unique hash based on
    an unique integer using the short_url PyPI package
    (https://pypi.org/project/short_url/).
    """

    # pylint: disable=too-few-public-methods
    @staticmethod
    def encode(unique_key):
        """
        Static method to generate a unique hash based on
        an unique integer.

        Args:
            unique_key: Unique integer based upon which a
                unique hash will be generated

        Returns:
            Unique hash

        Raises:
            TypeError: if the unique_key arg is not an integer
        """
        return short_url.encode_url(unique_key)


class FullURL:
    """
    Class to reverse generate the integer based on which
    the unique hash was generated using the short_url PyPI package
    (https://pypi.org/project/short_url/).
    """

    # pylint: disable=too-few-public-methods
    @staticmethod
    def decode(shorturl):
        """
        Static method to reverse generate the integer based
        on which the unique hash was generated.

        Args:
            shorturl: Unique hash which was generated based on
                a unique integer

        Returns:
            Unique integer

        Raises:
            ValueError: if the shorturl passed was not generated using
                the short_url package
        """
        return short_url.decode_url(shorturl)


class URLTransform:
    """
    Class responsible for calling the encode and decode wrappers
    and inserting, updating and retrieving the short_urls and full_urls
    from the database.
    """
    db_url = None
    original_url = None
    short_url_suffix = None

    def __init__(self) -> None:
        self.db_session = get_db_session()

    def encode(self, original_url):
        """
        Writes a new row to the database with the original_url,
        then uses the newly created row's id (which is unique)
        to generate a unique hash by calling the encode wrapper.
        Finally updates the database row with the generated hash.

        Args:
            original_url: The original URL which needs to be encoded

        Returns:
            The generated unique hash which is to be used as the short
            URL suffix.
        """
        self.original_url = original_url

        # generate unique integer
        unique_integer = self.db_insert()

        # generate unique short url
        self.short_url_suffix = ShortURL.encode(
            unique_key=unique_integer)

        # persist generated short url to database
        self.db_update()

        logger.debug(self.short_url_suffix)

        return self.short_url_suffix

    def db_insert(self, ):
        """
        Writes a new row to the database with the original_url.

        Returns:
            Newly created row's id.
        """
        self.db_url = URLsMap()
        self.db_url.original_url = self.original_url
        self.db_session.add(self.db_url)
        self.db_session.commit()
        logger.debug(self.db_url.id)
        return self.db_url.id

    def db_update(self, ):
        """
        Updates the database row with the generated hash.
        """
        self.db_url.short_url = self.short_url_suffix
        self.db_session.add(self.db_url)
        self.db_session.commit()

    def decode(self, short_url_suffix):
        """
        Reverse generates the integer used to generate the hash using
        the decode wrapper, looks up the database for the original URL
        with that integer as primary key.

        Args:
            short_url_suffix: The hash whose original URL needs to
                be looked up

        Returns:
            The original URL.

        Raises:
            ShortURL404: if either the short_url_suffix passed was not
                generated using the short_url package or if the integer generated
                does not exist in the database.
        """
        self.short_url_suffix = short_url_suffix

        try:
            url_id = FullURL.decode(self.short_url_suffix)
        except ValueError:
            logger.error(
                f'Unable to decode short_url: {self.short_url_suffix}.')
            # pylint: disable=raise-missing-from
            raise ShortURL404('Unable to decode short_url: {short_url}')

        # fetch the db_url object from db
        self.db_url = self.db_session.query(URLsMap).get(url_id)
        if not self.db_url:
            logger.error(
                f'short_url: {self.short_url_suffix} does not exist.')
            # pylint: disable=raise-missing-from
            raise ShortURL404('{short_url} does not exist')

        # logger.debug(self.db_url)
        logger.debug(self.db_url.original_url)

        return self.db_url.original_url
