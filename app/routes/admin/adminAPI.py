from flask_restful import Resource

from app.models.models import User, Addproduct, Brand, Category
from .form import RegistrationForm, LoginForm

from flask import session, request, render_template, Response, flash, redirect, url_for

from ...models.models import db
from ...routes import bcrypt



class AdminResource(Resource):
    def get(self):
        products = Addproduct.query.all()
        html_content=render_template('admin/index.html', title='Admin', products=products)
        return Response(html_content,content_type="text/html")


class AdminBrandResource(Resource):
    def get(self):
        brands = Brand.query.order_by(Brand.id.desc()).all()
        html_content = render_template('admin/brands.html',title='Brands', brands=brands)
        return Response(html_content,content_type="text/html")

       
  

class AdminCategoryResource(Resource):
    def get(self):
        categories = Category.query.order_by(Category.id.desc()).all()
        # return {'title': 'Categories', 'categories': [category.serialize() for category in categories]}
        html_content = render_template('admin/categories.html', title='Categories', categories=categories)
        return Response(html_content,content_type="text/html")


class AdminRegistrationResource(Resource):
    def post(self):
        form_data = request.get_json()
        form = RegistrationForm(data=form_data)
        if form.validate_on_submit():
            hash_password = bcrypt.generate_password_hash(form_data['password'])
            user = User(name=form_data['name'], username=form_data['username'], email=form_data['email'],
                        password=hash_password)
            db.session.add(user)
            flash(f'welcome {form.name.data} Thanks for registering','success')
            db.session.commit()
            return redirect(url_for('api_bp.AdminLoginResource'))
        html_content = render_template('admin/register.html', title='Register', form=form)
        return Response(html_content,content_type="text/html")
    

class AdminLoginResource(Resource):
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['username'] = user.username
                flash(f'welcome {user.name} you are logged in now','success')
                return redirect(url_for('api_bp.AdminResource'))
            else:
                flash(f'Login Unsuccessful. Please check username and password','danger')
                return redirect(url_for('api_bp.AdminLoginResource'))
        html_content = render_template('admin/login.html', title='Login', form=form)
        return Response(html_content,content_type="text/html")
             

         
       
        # return {'errors': form.errors}, 400
