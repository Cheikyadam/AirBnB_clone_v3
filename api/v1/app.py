#!/usr/bin/python3
"""app v1"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app_context(exception=None):
    """tear down"""
    storage.close()


if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        host = '0.0.0.0'
    else:
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        port = 5000
    else:
        port = getenv("HBNB_API_PORT")

    app.run(host=host, port=port, threaded=True)
