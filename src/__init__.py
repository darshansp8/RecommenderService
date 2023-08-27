from flask import Flask
from flask_cors import CORS
from src.recommendation_engine import recommend_blueprint
from src.mongo import getdata

import os


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"*": {'origins': '*', 'methods': ['OPTIONS', 'GET', 'POST', 'DELETE', 'PUT']}})

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
        )

    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(recommend_blueprint)
    app.register_blueprint(getdata)

    return app
