import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_restful import Api


db = SQLAlchemy()
api = Api()


def create_app(test_config=None, db=db, api=api):
    # Load environment variables from .env file
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
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

    
    #initialize the database
    db.init_app(app)
    #initialize the api
    api.init_app(app)


#    #Register the models
#     from .models import User, Category, Product, Order, Cart
    


    #Register api resources
    from .Resources.resource import CategoryResource, ProductResource, UserAuthResource, OrderResource, CartResource
    api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
    api.add_resource(ProductResource, '/api/products', '/api/products/<int:product_id>')
    api.add_resource(UserAuthResource, '/api/users', '/api/users/<int:user_id>')
    api.add_resource(OrderResource, '/api/orders', '/api/orders/<int:order_id>')
    api.add_resource(CartResource, '/api/cart', '/api/cart/<int:cart_id>')





    return app
