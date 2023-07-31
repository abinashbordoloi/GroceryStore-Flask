#file path : E:\projects\GrossaryStore\app\routes\frontend.py

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from flask import session



frontend_bp = Blueprint('frontend_bp', __name__)







# Define the main app routes to render templates or redirect to other routes
@frontend_bp.route('/')
def index():
    return render_template('base.html')


@frontend_bp.route('/dashboard')
def dashboard():
    return render_template('home.html')