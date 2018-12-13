from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import yaml

######### Enable this for debugging #########
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# SQLALCHEMY_TRACK_MODIFICATIONS = True
######## Enable this for debugging #########

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shend:root@localhost/ecommerce'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

######### Required in Case of firing complex queries without ORM #########
db2 = yaml.load(open('config.yaml'))
app.config['MYSQL_HOST'] = db2['mysql_host']
app.config['MYSQL_USER'] = db2['mysql_user']
app.config['MYSQL_PASSWORD'] = db2['mysql_password']
app.config['MYSQL_DB'] = db2['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
######### Required in Case of firing complex queries without ORM #########


# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
#
from ecommerce import models
from ecommerce import routes

models.db.create_all()