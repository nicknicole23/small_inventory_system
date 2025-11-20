"""
Flask extensions initialization.
All Flask extensions should be initialized here to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
cors = CORS()
