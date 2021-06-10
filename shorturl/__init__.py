"""
Bootstrap the Flask application,
Works as factory and provides instance of app.
"""

import os
from flask import Flask
from flasgger import Swagger
from shorturl.blueprints import shorturl_bp
from . import db


def create_app(test_config=None):
    """
    Flask app factory.
    Loads configs.
    Sets up logging.
    Defines routes.
    Initializes app.

    Args:
        test_config: test config to be passed while running tests

    Returns:
        Flask app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # pylint: disable=unused-variable
    swagger = Swagger(app)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'shortenurl.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_json('config.json', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(shorturl_bp)

    return app
