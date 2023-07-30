import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_restful import Api

# initialize the database
db = SQLAlchemy()
from .resources import api as resources_api





def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        # SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'GroveEase.db'),
        DEBUG=True,
    )
    #print the SQLALCHEMY_DATABASE_URI
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    


    #import models
    from .models import  User, Category, Product, Order, Cart



    #initialize the database
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            db.session.commit()
            print("Tables created successfully.")
        except Exception as e:
            print("Error creating tables:", e)
        
    
   

    
    

    from .resources import resources_bp
    app.register_blueprint(resources_bp)

    # Add the API resource routes
    resources_api.init_app(app)

    @app.route('/test')
    def test_route():
        return 'This is a test route.'
    
    




    return app
