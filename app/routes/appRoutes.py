from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from flask import session
import os


homeRoute_bp = Blueprint('homeRoute_bp', __name__)

@homeRoute_bp.route('/')
def home():
    # Check if the user is signed in by looking for the 'user_signed_in' key in the session
    show_sign_in_button = not session.get('user_signed_in', False)

    # Get the user's name from the session if the user is signed in
    user_name = session.get('user_name', 'Guest')

    # Render the home.html template and pass the data as variables to the template
    return render_template('home.html', showSignInButton=show_sign_in_button, userName=user_name)
