from flask import Flask, render_template

from config import Config

from .extensions import db
from .extensions import login_manager
from .extensions import csrf
from .models import User


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    csrf.init_app(app)


    @app.route("/")
    def index():

        return render_template("index.html")

    from .routes.auth import auth
    app.register_blueprint(auth)

    from .routes.student import student
    app.register_blueprint(student)
    
    from .routes.admin import admin
    app.register_blueprint(admin)
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404
    return app