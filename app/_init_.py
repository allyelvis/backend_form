from flask import Flask
from app.routes import main
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # CSRF protection
    csrf.init_app(app)

    app.register_blueprint(main)

    return app
