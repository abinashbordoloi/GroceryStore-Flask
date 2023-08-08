# from app import db
# from datetime import datetime


# #User Model




#     # User Model
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     role = db.Column(db.String(100), nullable=False)
#     def serialize(self):
#        return {
#            'id': self.id,
#            'name': self.name,
#            'description': self.description
#            # Add more attributes as needed
#        }
#    # Add more attributes as needed (e.g., first_name, last_name, etc.)
#     def check_password(self, password):
#         return password == self.password
   
# #create a instance of the user class
# # user = User(username='admin', password='admin', email='admin', role='admin')
# # #add the user to the database
# # db.session.add(user)
# # #commit the changes
# # db.session.commit()
# #


# #Category Model
# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text)
#     products = db.relationship('Product', back_populates='category', lazy=True)
#     # Add more attributes as needed (e.g., first_name, last_name, etc.)
#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description

#             # Add more attributes as needed
#         }

# # #Product Model
# # class Product(db.Model):
# #     __tablename__ = 'products'

# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(200), nullable=False)
# #     description = db.Column(db.Text)
# #     price = db.Column(db.Float, nullable=False)

# #Order model
# # class Order(db.Model):
# #     __tablename__ = 'orders'
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
# #     quantity = db.Column(db.Integer, nullable=False)
# #     # Add more attributes as needed (e.g., order_date, status, etc.)



# #Cart model
# class Cart(db.Model):
#     __tablename__ = 'cart'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

#     # Defer the configuration of the 'product' relationship until later
#     product = db.relationship('Product', back_populates='cart_items')

#     quantity = db.Column(db.Integer, nullable=False)
#     # Add more attributes as needed (e.g., order_date, status, etc.)
#     def serialize(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'product_id': self.product_id,
#             'quantity': self.quantity
#         }






# #Many to many relationship between Order and Product
# class Order(db.Model):
#     __tablename__ = 'order'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     order_date = db.Column(db.DateTime, default=datetime.utcnow)

#     # Define a one-to-many relationship with OrderItem
#     order_items = db.relationship('OrderItem', back_populates='order')    



# #Many to many relationship between Order and Product
# class Product(db.Model):
#     __tablename__ = 'product'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     manufacture_date = db.Column(db.Date, nullable=True)
#     expiry_date = db.Column(db.Date, nullable=True)
#     rate_per_unit = db.Column(db.Float, nullable=False)
#     unit_of_measurement = db.Column(db.String(20), nullable=False)

#     # Store the available quantity of the product
#     quantity = db.Column(db.Integer, default=0, nullable=False)

#     # Define a many-to-one relationship with Category
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
#     category = db.relationship('Category', back_populates='products')

#     # Define a many-to-one relationship with Cart
#     cart_items = db.relationship('Cart', back_populates='product')
#     # Define a one-to-many relationship with OrderItem
#     order_items = db.relationship('OrderItem', back_populates='product')




# #Many to many relationship between Order and Product
# class OrderItem(db.Model):
#     __tablename__ = 'order_item'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)

#     # Define a many-to-one relationship with Order
#     order = db.relationship('Order', back_populates='order_items')

#     # Define a many-to-one relationship with Product
#     product = db.relationship('Product', back_populates='order_items')
    


from app import db
from datetime import datetime
from flask_login import UserMixin
import json

class User(db.Model):


    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username




class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    # state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    zipcode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice




class Addproduct(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Brand %r>' % self.name
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name



    

