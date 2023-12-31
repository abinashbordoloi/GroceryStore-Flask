from flask import Flask, request, make_response, render_template, session, flash
from flask_restful import Api, Resource
from app.models.models import Register,CustomerOrder
#how to import stripe in flask
import stripe
from flask_login import login_required, current_user
from ...models.models import db
#how to import pdfkit in flask
import pdfkit
import secrets


# Define your resource classes




class PaymentResource(Resource):
    def post(self  ):
        data = request.get_json()
        invoice = data.get('invoice')
        amount = data.get('amount')
        customer = stripe.Customer.create(
            email=data.get('stripeEmail'),
            source=data.get('stripeToken'),
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            description='Myshop',
            amount=amount,
            currency='usd',
        )
        orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        orders.status = 'Paid'
        db.session.commit()
        return {'message': 'Payment successful'}, 200
    


class ThanksResource(Resource):
    def get(self):
        return render_template('customer/thank.html')




class UpdateShoppingCartResource(Resource):
    @login_required
    def post(self):
        shopping_cart = session.get('Shoppingcart')
        if shopping_cart:
            for key, shopping in shopping_cart.items():
                shopping.modified = True
                del shopping['image']
                del shopping['colors']
            return {'message': 'Shopping cart updated'}, 200
        else:
            return {'error': 'Shopping cart not found'}, 404

class GetOrderResource(Resource):
    @login_required
    def get(self):
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        shopping_cart = session.get('Shoppingcart')
        if shopping_cart:
            try:
                order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=shopping_cart)
                db.session.add(order)
                db.session.commit()
                session.pop('Shoppingcart')
                return {'message': 'Your order has been sent successfully'}, 200
            except Exception as e:
                print(e)
                return {'error': 'Something went wrong while processing the order'}, 500
        else:
            return {'error': 'Shopping cart not found'}, 404

class OrdersResource(Resource):
    @login_required
    def get(self, invoice):
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        if orders:
            grandTotal = 0
            subTotal = 0
            for _key, product in orders.orders.items():
                discount = (product['discount'] / 100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = "%.2f" % (0.06 * float(subTotal))
                grandTotal = "%.2f" % (1.06 * float(subTotal))
            return {'customer': customer, 'orders': orders.orders, 'tax': tax, 'subTotal': subTotal, 'grandTotal': grandTotal}, 200
        else:
            return {'error': 'Orders not found'}, 404

class GetPdfResource(Resource):
    @login_required
    def post(self, invoice):
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        if orders:
            grandTotal = 0
            subTotal = 0
            for _key, product in orders.orders.items():
                discount = (product['discount'] / 100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = "%.2f" % (0.06 * float(subTotal))
                grandTotal = float("%.2f" % (1.06 * subTotal))
            rendered = render_template('customer/pdf.html', invoice=invoice, tax=tax, grandTotal=grandTotal, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inline; filename=' + invoice + '.pdf'
            return response, 200
        else:
            return {'error': 'Orders not found'}, 404