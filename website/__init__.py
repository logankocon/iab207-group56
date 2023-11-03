#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    db.init_app(app)

    Bootstrap5(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #imports login manager
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
         return User.query.get(int(user_id))

    # registers all the bookmarks
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import events
    app.register_blueprint(events.event_bp)

    from . import events
    app.register_blueprint(events.edit_bp)

    @app.errorhandler(404) 
    def not_found(e): 
      return render_template("404.html", error=e)

    @app.errorhandler(500) 
    def not_found(e): 
      return render_template("50x.html", error=e)
    
    return app