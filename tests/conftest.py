"""
Module to define pytest fixtures
"""
import os
import tempfile

import pytest

from shorturl import create_app
from shorturl.db import init_db


@pytest.fixture(scope='module')
def client():
    # pylint: disable=redefined-outer-name
    """
    Sets up the database as a temporary memory file.
    """
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
