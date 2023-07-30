# resources/__init__.py
from flask import Blueprint
from flask_restful import Api

# Create a Blueprint for the resources
resources_bp = Blueprint('resources', __name__)

# Create an instance of the Api
api= Api()

# Import resource classes to register them with the Api
from .resource import (
    CategoryResource,
    ProductResource,
    UserAuthResource,
    OrderResource,
    CartResource,
    HelloWorld,
)

# Add resource classes to the Api
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
api.add_resource(ProductResource, '/api/products', '/api/products/<int:product_id>')
api.add_resource(UserAuthResource, '/api/users', '/api/users/<int:user_id>')
api.add_resource(OrderResource, '/api/orders', '/api/orders/<int:order_id>')
api.add_resource(CartResource, '/api/cart', '/api/cart/<int:cart_id>')
api.add_resource(HelloWorld, '/api/hello')
