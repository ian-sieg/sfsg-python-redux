from flask import Flask
from flask_cors import CORS
from .routes import api
from .db import init_db
from dotenv import load_dotenv
from os import getenv
from flask_jwt_extended import JWTManager

load_dotenv()
secret = getenv('SECRET_KEY')
# test_config=None

def create_app(config_file=None):
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
    app.url_map.strict_slashes = False
    
    app.config["SECRET_KEY"] = secret
    app.config["JWT_SECRET_KEY"] = 'supersecretsecretkey'
    
    CORS(app)
    JWTManager(app)
    
    app.register_blueprint(api)    
    
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    init_db(app)
    return app

# if __name__ == "__main__":
#     app.run(debug=True)