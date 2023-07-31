from flask import Blueprint, render_template, request, redirect, url_for
from flask import session


#for the login landing page
login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login')
def login_page():
    return render_template('loginLanding.html')   


@login_bp.route('/user_login')
def user_login():
    return render_template('user/userLogin.html')



@login_bp.route('/admin_login')
def admin_login():
    return render_template('admin/adminLogin.html')



@login_bp.route('/userauth', methods=['POST'])
def user_auth():
    if request.method == 'POST':
        # Get username and password from the form data using the get method with default empty strings
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Send the username and password to the UserAuthResource to authenticate the user
        from app.resources.resource import UserAuthResource
       
        auth_response = UserAuthResource.post(username=username, password=password)
        if auth_response.status_code == 200:
            # User is authenticated, redirect to the dashboard
            return redirect(url_for('frontend_bp.dashboard'))
        else:
            # Authentication failed, show an error message
            error_message = 'Invalid username or password. Please try again.'
            return render_template('user/userLogin.html', error_message=error_message)
