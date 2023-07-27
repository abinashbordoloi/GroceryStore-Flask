from flask import Blueprint, render_template, request, redirect, url_for

from flask import session

from app.models import User


#for the login landing page
login_bp = Blueprint('login_bp', __name__)
@login_bp.route('/login')
def login():
    return render_template('loginLanding.html')





#for the admin login page form
admin_bp = Blueprint('admin_bp', __name__)
@admin_bp.route('/admin_login')
def admin_login():
    return render_template('admin/adminLogin.html')





#for the user login page form
user_bp = Blueprint('user_bp', __name__)
@user_bp.route('/user_login')
def user_login():
    return render_template('user/userLogin.html')






# for the userAuth for both user and admin
userAuth_bp = Blueprint('userAuth_bp', __name__)

@userAuth_bp.route('/userAuth', methods=['GET', 'POST'])
def userAuth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # current_directory = os.path.dirname(__file__)
        # database_path = os.path.join(current_directory, 'instance', 'GroveEase.sqlite')

        try:
            # Connect to the database and verify the user's credentials
            # conn = sqlite3.connect(database_path)
            # cursor = conn.cursor()
            # cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            # user = cursor.fetchone()
            # conn.close()
           user = User.query.filter_by(username=username, password=password).first()
           if user:
                # User is authenticated, create a user session
                session['user_id'] = user.id  # Store the user ID in the session
                session['user_name'] = user.usernmae  # Store the username in the session
                session['user_signed_in'] = True

                return redirect(url_for('home'))
           else:
                # Invalid credentials, show an error message on the loginLanding page
                error_message = 'Invalid username or password. Please try again.'
                return render_template('loginLanding.html', error_message=error_message)

        except Exception as e:
            # Handle database connection error, show an error message on the loginLanding page
            error_message = f"Database error: {e}"
            return render_template('loginLanding.html', error_message=error_message)

    return render_template('loginLanding.html')
