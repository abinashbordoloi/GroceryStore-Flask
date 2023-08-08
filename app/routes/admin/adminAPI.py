from flask_restful import Resource
from app import db, bcrypt
from app.models import User, Addproduct, Brand, Category
from .form import RegistrationForm, LoginForm

from flask import session, request



class AdminResource(Resource):
    def get(self):
        products = Addproduct.query.all()
        return {'title': 'Admin page', 'products': [product.serialize() for product in products]}

class BrandResource(Resource):
    def get(self):
        brands = Brand.query.order_by(Brand.id.desc()).all()
        return {'title': 'Brands', 'brands': [brand.serialize() for brand in brands]}

class CategoryResource(Resource):
    def get(self):
        categories = Category.query.order_by(Category.id.desc()).all()
        return {'title': 'Categories', 'categories': [category.serialize() for category in categories]}

class RegistrationResource(Resource):
    def post(self):
        form_data = request.get_json()
        form = RegistrationForm(data=form_data)
        if form.validate_on_submit():
            hash_password = bcrypt.generate_password_hash(form_data['password'])
            user = User(name=form_data['name'], username=form_data['username'], email=form_data['email'],
                        password=hash_password)
            db.session.add(user)
            db.session.commit()
            return {'message': f'Welcome {form_data["name"]}! Thanks for registering'}
        return {'errors': form.errors}, 400

class LoginResource(Resource):
    def post(self):
        form_data = request.get_json()
        form = LoginForm(data=form_data)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form_data['email']).first()
            if user and bcrypt.check_password_hash(user.password, form_data['password']):
                session['email'] = form_data['email']
                return {'message': f'Welcome {form_data["email"]}! You are logged in now'}
            return {'message': 'Wrong email and password'}, 401
        return {'errors': form.errors}, 400
