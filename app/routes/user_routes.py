from flask import ( render_template , Blueprint )

user_bp = Blueprint('user_bp', __name__)





@user_bp.route('/user_login')
def user_login():
    return render_template('user/userLogin.html')

