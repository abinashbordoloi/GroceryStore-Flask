from typing import Any
from flask_restful import Resource
from flask import render_template, Response

class AppResource(Resource):
    def get(self):
      # Render the admin login page template
      html_content = render_template('navbar.html')
      return Response(html_content, mimetype="text/html")

    

    
class LoginResource(Resource):
    def get(self):
        # Render the admin login page template
        return render_template('loginLanding.html')
    
  

class UserResource(Resource):
    def get(self):
      # Render the admin login page template
      return render_template('user/userLogin.html')
    
      
    
    def post(self):
        return {'hello': 'world'}
    
    def put(self):
        return {'hello': 'world'}
    
    def delete(self):
        return {'hello': 'world'}
    
    def patch(self):
        return {'hello': 'world'}
    
    def options(self):
        return {'hello': 'world'}
    
    def head(self):
        return {'hello': 'world'}
    
    def trace(self):
        return {'hello': 'world'}
    
    def connect(self):
        return {'hello': 'world'}
    
    def any(self):
        return {'hello': 'world'}
    
    def view(self):
        return {'hello': 'world'}
    
    def search(self):
        return {'hello': 'world'}
    
    def find(self):
        return {'hello': 'world'}
    
    def locate(self):
        return {'hello': 'world'}
    
    def discover(self):
        return {'hello': 'world'}
    










class AdminResource(Resource):
    def get(self):
      # Render the admin login page template
      return render_template('admin/adminLogin.html')
    
      
    
    def post(self):
        return {'hello': 'world'}
    
    def put(self):
        return {'hello': 'world'}
    
    def delete(self):
        return {'hello': 'world'}
    
    def patch(self):
        return {'hello': 'world'}
    
    def options(self):
        return {'hello': 'world'}
    
    def head(self):
        return {'hello': 'world'}
    
    def trace(self):
        return {'hello': 'world'}
    
    def connect(self):
        return {'hello': 'world'}
    
    def any(self):
        return {'hello': 'world'}
    
    def view(self):
        return {'hello': 'world'}
    
    def search(self):
        return {'hello': 'world'}
    
    def find(self):
        return {'hello': 'world'}
    
    def locate(self):
        return {'hello': 'world'}
    
    def discover(self):
        return {'hello': 'world'}