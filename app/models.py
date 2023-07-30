from app import db
from datetime import datetime


#User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
            # Add more attributes as needed
        }
    # Add more attributes as needed (e.g., first_name, last_name, etc.)


#Category Model
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', back_populates='category', lazy=True)
    # Add more attributes as needed (e.g., first_name, last_name, etc.)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description

            # Add more attributes as needed
        }

# #Product Model
# class Product(db.Model):
#     __tablename__ = 'products'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text)
#     price = db.Column(db.Float, nullable=False)

#Order model
# class Order(db.Model):
#     __tablename__ = 'orders'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     # Add more attributes as needed (e.g., order_date, status, etc.)



#Cart model
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Defer the configuration of the 'product' relationship until later
    product = db.relationship('Product', back_populates='cart_items')

    quantity = db.Column(db.Integer, nullable=False)
    # Add more attributes as needed (e.g., order_date, status, etc.)
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }






#Many to many relationship between Order and Product
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Define a one-to-many relationship with OrderItem
    order_items = db.relationship('OrderItem', back_populates='order')    


#Many to many relationship between Order and Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.Date, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    rate_per_unit = db.Column(db.Float, nullable=False)
    unit_of_measurement = db.Column(db.String(20), nullable=False)

    # Store the available quantity of the product
    quantity = db.Column(db.Integer, default=0, nullable=False)

    # Define a many-to-one relationship with Category
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', back_populates='products')

    # Define a many-to-one relationship with Cart
    cart_items = db.relationship('Cart', back_populates='product')
    # Define a one-to-many relationship with OrderItem
    order_items = db.relationship('OrderItem', back_populates='product')




#Many to many relationship between Order and Product
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define a many-to-one relationship with Order
    order = db.relationship('Order', back_populates='order_items')

    # Define a many-to-one relationship with Product
    product = db.relationship('Product', back_populates='order_items')
    

