"""
Module responsible for initializing the database
and provide a database session for SQLAlchemy operations
"""
# pylint: disable=invalid-name

import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db():
    """
    Creates an SQLite connection, and stores it for
    later reuse.

    Returns:
        sqlite3.connect object
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # pylint: disable=unused-argument
    """
    Closes the sqlite3.connect object and removes it from the
    g special object.

    Args:
        e: error object to pass errors if required

    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initializes the SQLite database, clears exising data and
    migrates tables for first time use. Reads from `schema.sql`.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    CLI wrapper over `init_db`.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Calls `close_db` when cleaning up after returning the response.
    Adds the `init-db` command to be called with `flask init-db`.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db_session():
    """
    Creates a SQLite db_session to be used with SQLAlchemy models

    Returns:
        SQLAlchemy session
    """
    db_engine = create_engine(
        f'sqlite:///{current_app.config["DATABASE"]}',
    )
    return sessionmaker(bind=db_engine, autocommit=False)()
