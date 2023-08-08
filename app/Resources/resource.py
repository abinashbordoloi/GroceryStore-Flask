from flask_restful import Resource, reqparse
from ..models import *
from flask import jsonify, request, make_response, g
from app import db


# test api
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, this is a simple API!'}


class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if category:
                return jsonify(category.serialize())
            else:
                return jsonify({'message': 'Category not found'}), 404
        else:
            categories = Category.query.all()
            return jsonify([category.serialize() for category in categories])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Category name is required')
        parser.add_argument('description', type=str, required=True,
                            help='Category description is required')
        args = parser.parse_args()

        category = Category(name=args['name'], description=args['description'])

        db.session.add(category)
        db.session.commit()

        return {'message': 'Category created successfully', 'category': category.serialize()}, 201

    def put(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Category name is required')
        parser.add_argument('description', type=str, required=True,
                            help='Category description is required')
        args = parser.parse_args()

        category.name = args['name']
        category.description = args['description']
        db.session.commit()

        return {'message': 'Category updated successfully', 'category': category.serialize()}

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category not found'}, 404

        # Check if the category has associated products
        if category.products:
            return jsonify({'message': 'Cannot delete category with associated products'}), 400

        db.session.delete(category)
        db.session.commit()

        return {'message': 'Category deleted successfully'}, 204


class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return jsonify(product.serialize())
            else:
                return {'message': 'Product not found'}, 404
        else:
            products = Product.query.all()
            return jsonify([product.serialize() for product in products])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Product name is required')
        parser.add_argument('manufacture_date', type=str,
                            required=True, help='Manufacture date is required')
        parser.add_argument('expiry_date', type=str,
                            required=True, help='Expiry date is required')
        parser.add_argument('rate_per_unit', type=float,
                            required=True, help='Rate per unit is required')
        parser.add_argument('category_id', type=int,
                            required=True, help='Category ID is required')
        args = parser.parse_args()

        product = Product(name=args['name'], manufacture_date=args['manufacture_date'],
                          expiry_date=args['expiry_date'], rate_per_unit=args['rate_per_unit'],
                          category_id=args['category_id'])

        db.session.add(product)
        db.session.commit()

        return {'message': 'Product created successfully', 'product': product.serialize()}, 201

    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Product name is required')
        parser.add_argument('manufacture_date', type=str,
                            required=True, help='Manufacture date is required')
        parser.add_argument('expiry_date', type=str,
                            required=True, help='Expiry date is required')
        parser.add_argument('rate_per_unit', type=float,
                            required=True, help='Rate per unit is required')
        parser.add_argument('category_id', type=int,
                            required=True, help='Category ID is required')
        args = parser.parse_args()

        product.name = args['name']
        product.manufacture_date = args['manufacture_date']
        product.expiry_date = args['expiry_date']
        product.rate_per_unit = args['rate_per_unit']
        product.category_id = args['category_id']

        db.session.commit()

        return {'message': 'Product updated successfully', 'product': product.serialize()}

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        db.session.delete(product)
        db.session.commit()

        return {'message': 'Product deleted successfully'}, 204


# Helper function to check if the current user is authenticated
def login_required(func):
    def wrapper(*args, **kwargs):
        if not g.user:
            return {'message': 'Authentication required'}, 401
        return func(*args, **kwargs)
    return wrapper





    
#User authentication
class UserAuthResource(Resource):
    #should have a post method
    def post(self, username, password):
        #get the username and password from the request
        username = request.form['username']
        password = request.form['password']
        



        #check if the user exists in the database
        user = User.query.filter_by(username).first()
        if user and user.check_password(password):
            return user
        else:
            print("Invalid username or password")

            return None
        #if the user exists, check if the password is correct

        #if the password is correct, return the user object
        #if the password is incorrect, return None
        #if the user does not exist, return None
        #return None
        
        


    

          
        
        


        
       

        
      


class CartResource(Resource):
    @login_required
    def get(self):
        cart_items = Cart.query.filter_by(user_id=g.user.id).all()
        return jsonify([item.serialize() for item in cart_items])

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('product_id', type=int,
                            required=True, help='Product ID is required')
        parser.add_argument('quantity', type=int,
                            required=True, help='Quantity is required')
        args = parser.parse_args()

        product = Product.query.get(args['product_id'])
        if not product:
            return {'message': 'Product not found'}, 404

        cart_item = Cart.query.filter_by(
            user_id=g.user.id, product_id=args['product_id']).first()
        if cart_item:
            cart_item.quantity += args['quantity']
        else:
            cart_item = Cart(
                user_id=g.user.id, product_id=args['product_id'], quantity=args['quantity'])

        db.session.add(cart_item)
        db.session.commit()

        return {'message': 'Product added to cart successfully', 'cart_item': cart_item.serialize()}, 201

    @login_required
    def put(self, cart_item_id):
        cart_item = Cart.query.filter_by(
            id=cart_item_id, user_id=g.user.id).first()
        if not cart_item:
            return {'message': 'Cart item not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int,
                            required=True, help='Quantity is required')
        args = parser.parse_args()

        cart_item.quantity = args['quantity']
        db.session.commit()

        return {'message': 'Cart item updated successfully', 'cart_item': cart_item.serialize()}

    @login_required
    def delete(self, cart_item_id):
        cart_item = Cart.query.filter_by(
            id=cart_item_id, user_id=g.user.id).first()
        if not cart_item:
            return {'message': 'Cart item not found'}, 404

        db.session.delete(cart_item)
        db.session.commit()

        return {'message': 'Cart item deleted successfully'}, 204


class OrderResource(Resource):
    @login_required
    def get(self):
        # Get all orders of the authenticated user
        user_id = g.user.id
        orders = Order.query.filter_by(user_id=user_id).all()

        # Return a list of orders with details
        order_list = []
        for order in orders:
            order_data = {
                'id': order.id,
                'user_id': order.user_id,
                'order_date': order.order_date,
                # Add more details as needed
            }
            order_list.append(order_data)

        return {'orders': order_list}

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('products', type=list,
                            required=True, help='Products list is required')
        args = parser.parse_args()

        # Create a new order for the authenticated user
        user_id = g.user.id
        order = Order(user_id=user_id)
        db.session.add(order)

        # Add selected products to the order with quantities
        for product_data in args['products']:
            product_id = product_data['product_id']
            quantity = product_data['quantity']

            # Deduct the product quantities from the inventory
            product = Product.query.get(product_id)
            if product and product.quantity >= quantity:
                product.quantity -= quantity
                db.session.add(product)

                # Add the product to the order_items table
                order_item = OrderItem(
                    order=order, product=product, quantity=quantity)
                db.session.add(order_item)
            else:
                # If the product is out of stock or insufficient quantity, return an error message
                return {'message': 'Product out of stock or insufficient quantity'}, 400

        # Commit the changes to the database
        db.session.commit()

        # Return success message
        return {'message': 'Order placed successfully'}
