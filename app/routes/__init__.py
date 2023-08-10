from flask import Blueprint
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_msearch import Search

from flask_reuploads import UploadSet, IMAGES

api_bp  = Blueprint('api_bp', __name__)


bcrypt = Bcrypt()
search = Search()
photos = UploadSet('photos', IMAGES)





# Create an instance of the Api
api= Api(api_bp)

# Import the resources to add routes to the api
from .admin.adminAPI import AdminResource, AdminBrandResource, AdminCategoryResource, AdminRegistrationResource, AdminLoginResource
from .products.productAPI import ProductResource, ProductBrandResource, ProductCategoryResource



# Register your Admin-related Resource classes with URLs
api.add_resource(AdminResource, '/admin')
api.add_resource(AdminBrandResource, '/admin/brands')
api.add_resource(AdminCategoryResource, '/admin/categories')
api.add_resource(AdminRegistrationResource, '/admin/register')
api.add_resource(AdminLoginResource, '/admin/login')

api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
api.add_resource(ProductBrandResource, '/brands/<int:brand_id>')
api.add_resource(ProductCategoryResource, '/categories/<int:category_id>')
# Import the resources to add routes to the api





