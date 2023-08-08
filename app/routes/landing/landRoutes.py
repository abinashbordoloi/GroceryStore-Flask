#file path : E:\projects\GrossaryStore\app\routes\frontend.py

from flask import Blueprint, render_template, request, redirect, url_for



app_bp = Blueprint('app_bp', __name__)



# Define the main app routes to render templates or redirect to other routes
@app_bp.route('/')
def index():
    return render_template('base.html')


@app_bp.route('/login')
def login_page():
    return render_template('loginLanding.html')   



