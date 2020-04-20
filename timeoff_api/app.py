from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api

from database.db import initialize_db
from resources.errors import errors

import os

app = Flask(__name__)

DB_URI = os.environ.get('DB_URI', None)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', None)


if DB_URI and JWT_SECRET_KEY:
    app.config["MONGODB_HOST"] = DB_URI
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
else:
    app.config.from_envvar('ENV_FILE_LOCATION')


#app.config.from_envvar('ENV_FILE_LOCATION')
#mail = Mail(app)

# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app)
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)