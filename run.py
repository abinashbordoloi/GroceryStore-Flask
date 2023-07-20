# app.py

from app import create_app


# Create the Flask app instance using the create_app() function
app = create_app()

# Run the app using the Flask development server
if __name__ == '__main__':
    app.run()
