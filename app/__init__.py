import os


from dotenv import load_dotenv
from flask import Flask, render_template

def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'schema.sqlite'),
        DEBUG=True,  # Set the DEBUG configuration to True for development/testing
        # Other instance-specific configurations can be added here
    )

    if test_config is not None:
        # If test_config is provided, update the app's configuration with the test_config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('loginLanding.html')
    
 
    # from .routes.user_routes import user_bp
    # app.register_blueprint(user_bp)

    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    #for adiminLogin
    from .routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
   
    





    return app
