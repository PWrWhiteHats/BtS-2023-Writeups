import secrets

from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
jwt = JWTManager(app)
