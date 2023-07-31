import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask

# Initialize the database
db = SQLAlchemy()

def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'GroveEase.db'),
        DEBUG=True,
    )

    # Load the instance config, if it exists, when not testing
    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            db.session.commit()
            print("Tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)

    # Add the API resource routes
    from .resources import api as resources_api
    resources_api.init_app(app)

    # Add the frontend routes
    from .routes import frontend, userAuth
    app.register_blueprint(frontend.frontend_bp)
    app.register_blueprint(userAuth.login_bp)
    
    return app
