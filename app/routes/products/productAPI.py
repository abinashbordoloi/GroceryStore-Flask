from app.models.models import Register,CustomerOrder, Brand, Category, Addproduct
from ...models.models import db
from flask_restful import Resource, reqparse, marshal_with, fields, current_app
from flask import request, render_template, Response, flash, redirect, url_for, session, jsonify
import secrets,os
from .forms import Addproducts
from ...routes import photos,search



def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

# product_fields = {
#     'id': fields.Integer,
#     'name': fields.String,
#     'price': fields.Float,
#     'discount': fields.Integer,
#     'stock': fields.Integer,
#     'colors': fields.String,
#     'desc': fields.String,
#     'pub_date': fields.DateTime,
#     'category_id': fields.Integer,
#     'category': fields.String,
#     'brand_id': fields.Integer,
#     'brand': fields.String,
#     'image_1': fields.String,
#     'image_2': fields.String,
#     'image_3': fields.String,
# }

class ProductResource(Resource):
    def get(self, product_id):
        if product_id:
            product = Addproduct.qeury.get_or_404(product_id)
            html_content = render_template('products/single_page.html', title='Product', product=product, brands=brands(), categories=categories())
            return Response(html_content,content_type="text/html")
        else:
            page = request.args.get('page', 1, type=int)
            products = Addproduct.query.filter(Addproducts.stock>0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
            html_content = render_template('products/index.html', title='Products', products=products, brands=brands(), categories=categories())
            return Response(html_content,content_type="text/html")
        

    def post(self):
        form = Addproducts(request.form)
        brands = Brand.query.all()
        categories = Category.query.all()
        if request.method=="POST"and 'image_1' in request.files:
            name = form.name.data
            price = form.price.data
            discount = form.discount.data
            stock = form.stock.data
            colors = form.colors.data
            desc = form.discription.data
            brand = request.form.get('brand')
            category = request.form.get('category')
            image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            addproduct = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
            db.session.add(addproduct)
            flash(f'The product {name} was added in database','success')
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)
    
    def put(self, product_id):
        form = Addproducts(request.form)
        product = Addproduct.query.get_or_404(id)
        brands = Brand.query.all()
        categories = Category.query.all()
        brand = request.form.get('brand')
        category = request.form.get('category')
        if request.method =="POST":
            product.name = form.name.data 
            product.price = form.price.data
            product.discount = form.discount.data
            product.stock = form.stock.data 
            product.colors = form.colors.data
            product.desc = form.discription.data
            product.category_id = category
            product.brand_id = brand
            if request.files.get('image_1'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                    product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                except:
                    product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            if request.files.get('image_2'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                    product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
                except:
                    product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            if request.files.get('image_3'):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                    product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
                except:
                    product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

            flash('The product was updated','success')
            db.session.commit()
            return redirect(url_for('adminresource.get'))
        form.name.data = product.name
        form.price.data = product.price
        form.discount.data = product.discount
        form.stock.data = product.stock
        form.colors.data = product.colors
        form.discription.data = product.desc
        brand = product.brand.name
        category = product.category.name
        html_content = render_template('products/addproduct.html', form=form, title='Update Product', updateproduct=product, brands=brands, categories=categories, brand=brand, category=category)
        return Response(html_content,content_type="text/html")


    def delete(self, product_id):
        product = Addproduct.query.get_or_404(product_id)   
        if request.method =="POST":
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
            except Exception as e:
                print(e)
            db.session.delete(product)
            db.session.commit()
            flash(f'The product {product.name} was delete from your record','success')
            return redirect(url_for('adimresource.get'))
        flash(f'Can not delete the product','success')
        return redirect(url_for('adminresource.get'))
    


   
    def search(self):
        searchword = request.args.get('q')
        products = Addproduct.query.mysearch(searchword, fields=['name', 'desc'], limit=10)
        html_content = render_template('products/result.html', title='Search', products=products, brands=brands(), categories=categories())
        return Response(html_content,content_type="text/html")


class ProductBrandResource(Resource):
    def get(self, brand_id):
        page = request.args.get('page', 1, type=int)
        get_brand = Brand.query.filter_by(id=brand_id).first_or_404()
        products = Addproduct.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
        html_content = render_template('products/index.html', title='Products', products=products, brands=brands(), categories=categories())
        return Response(html_content,content_type="text/html")
    
    def post(self):
        if request.method =="POST":
            getbrand = request.form.get('brand')
            brand = Brand(name=getbrand)
            db.session.add(brand)
            flash(f'The brand {getbrand} was added to your database','success')
            db.session.commit()
            return redirect(url_for('AdminBrandResource.post'))
        html_content = render_template('admin/addbrand.html', title='Add Brand', brands= 'brands')
        return Response(html_content,content_type="text/html")
    
    def put(self, brand_id):
        if 'email' not in session:
            flash(f'Please login first', 'danger')
            return redirect(url_for('AdminLoginResource.post'))
        updatebrand = Brand.query.get_or_404(brand_id)
        brand = request.form.get('brand')
        if request.method =="POST":
            updatebrand.name = brand
            flash(f'Your brand has been updated','success')
            db.session.commit()
            return redirect(url_for('AdminBrandResource.get'))
       
        brand = updatebrand.name
        html_content = render_template('admin/addbrand.html', title='Update Brand', brand=brand, updatebrand=updatebrand)
        return Response(html_content,content_type="text/html")
    
    def delete(self, brand_id):
        category = Category.query.get_or_404(brand_id)
        if request.method=="POST":
            db.session.delete(category)
            flash(f"The brand {category.name} was deleted from your database","success")
            db.session.commit()
            return redirect(url_for('AdminBrandResource.get'))
        flash(f"The brand {category.name} can't be  deleted from your database","warning")
        return redirect(url_for('AdminBrandResource.get'))
    


class ProductCategoryResource(Resource):
    def get(self, category_id):
        page = request.args.get('page',1, type=int)
        get_cat = Category.query.filter_by(id=id).first_or_404()
        get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
        html_content = render_template('products/index.html', title='Products', products=get_cat_prod, brands=brands(), categories=categories())
        return Response(html_content,content_type="text/html")
       
    def post(self):
        if request.method =="POST":
            getcat = request.form.get('category')
            category = Category(name=getcat)
            db.session.add(category)
            flash(f'The brand {getcat} was added to your database','success')
            db.session.commit()
            return redirect(url_for('productcategoryresource.post'))
        html_content = render_template('admin/addcategory.html', title='Add Category', categories=categories())
        return Response(html_content,content_type="text/html")
    
    def put(self,category_id):
        if 'email' not in session:
            flash('Login first please','danger')
            return redirect(url_for('login'))
        updatecat = Category.query.get_or_404(category_id)
        category = request.form.get('category')  
        if request.method =="POST":
            updatecat.name = category
            flash(f'The category {updatecat.name} was changed to {category}','success')
            db.session.commit()
            return redirect(url_for('productcategoryresource.get'))
        category = updatecat.name
        html_content = render_template('admin/addcategory.html', title='Update Category', category=category, updatecat=updatecat)
        return Response(html_content,content_type="text/html")
    
    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        if request.method=="POST":
            db.session.delete(category)
            flash(f"The brand {category.name} was deleted from your database","success")
            db.session.commit()
            return redirect(url_for('adminresource.get'))
        flash(f"The brand {category.name} can't be  deleted from your database","warning")
        return redirect(url_for('adminresource.get'))

