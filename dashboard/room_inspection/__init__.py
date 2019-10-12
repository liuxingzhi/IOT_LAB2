from room_inspection.app import *
from .db import get_db
from flask import Flask, render_template, jsonify
import os, re


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "data.sqlite"),
    )
    with app.app_context():
        from . import db
        db.init_db()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def homepage():
        cur = get_db().cursor()
        cur.execute("SELECT DISTINCT ROOM_NUM FROM AIR_QUALITY_INDEX;")
        rooms = []
        for r in cur.fetchall():
            if r[0] is not None:
                rooms.append(r[0])
        return render_template('website.HTML')

    @app.route("/most_recent_data")
    def latest_data():
        # with get_db().cursor() as c:
        cur = get_db().cursor()
        cur.execute("SELECT * FROM AIR_QUALITY_INDEX WHERE id = (SELECT MAX(id) FROM AIR_QUALITY_INDEX);")
        air_quality = cur.fetchone()[1]
        cur.execute("SELECT * FROM MAC_NUM WHERE id = (SELECT MAX(id) FROM MAC_NUM);")
        mac_num = cur.fetchone()[1]
        data_dict = {"air_quality": air_quality, "mac_num": mac_num}
        return jsonify(data_dict)

    return app

# import os
#
# from flask import Flask, url_for
#
#
# def create_app(test_config=None):
#     """Create and configure an instance of the Flask application."""
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         # a default secret that should be overridden by instance config
#         SECRET_KEY="dev",
#         # store the database in the instance folder
#         DATABASE=os.path.join(app.instance_path, "data.sqlite"),
#     )
#
#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile("config.py", silent=True)
#     else:
#         # load the test config if passed in
#         app.config.update(test_config)
#
#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
# @app.route("/hello")
# def hello():
#     return render_template("website.HTML")
#
#     # register the database commands
#     from room_inspection import db
#
#     db.init_app(app)
#
#     # # apply the blueprints to the app
#     # from board import auth, blog
#     #
#     # app.register_blueprint(auth.bp)
#     # app.register_blueprint(blog.bp)
#     #
#     # # make url_for('index') == url_for('blog.index')
#     # # in another app, you might define a separate main index here with
#     # # app.route, while giving the blog blueprint a url_prefix, but for
#     # # the tutorial the blog will be the main index
#     app.add_url_rule("/", endpoint="hello")
#
#     # with app.test_request_context('/'):
#     #     print(url_for('foo_view'))
#     #     print(url_for('homepage'))
#     #     # url_for('bar_view') will raise werkzeug.routing.BuildError
#     #     # print(url_for('bar_view'))
#
#     return app
