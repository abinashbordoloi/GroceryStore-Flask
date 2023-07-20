from flask import ( render_template , Blueprint )

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin_login')
def admin_login():
    return render_template('admin/adminLogin.html')
