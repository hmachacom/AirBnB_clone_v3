#!/usr/bin/python3
"""Create a folder v1 inside api:
create an empty file __init__.py
"""
from models import storage
from os import getenv
from flask import Flask
from api.v1.views import app_views
from flask import jsonify, make_response


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage_new(self):
    """request you must remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")
    debug = getenv("HBNB_API_DEBUG", default=False)
    app.run(host=host, port=port, debug=debug, threaded=True)
