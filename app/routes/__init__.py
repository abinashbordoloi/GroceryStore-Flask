from flask import Blueprint
from flask_restful import Api

api_bp  = Blueprint('api_bp', __name__)





# Create an instance of the Api
api= Api(api_bp)

from .apiResource import (
    AppResource,
    UserResource,
    AdminResource,
    LoginResource
)

api.add_resource(AppResource, '/')
api.add_resource(LoginResource, '/login')
api.add_resource(UserResource, '/user/login', '/api/user/<int:user_id>',)
api.add_resource(AdminResource, '/admin/login', '/api/admin/<int:admin_id>',)






# # Add resource classes to the Api
# api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:category_id>')
# api.add_resource(ProductResource, '/api/products', '/api/products/<int:product_id>')
# api.add_resource(UserAuthResource, '/api/users', '/api/users/<int:user_id>')
# api.add_resource(OrderResource, '/api/orders', '/api/orders/<int:order_id>')
# api.add_resource(CartResource, '/api/cart', '/api/cart/<int:cart_id>')
# api.add_resource(HelloWorld, '/api/hello')
