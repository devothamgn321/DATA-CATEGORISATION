from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:6364600337@localhost/test?charset=utf8mb4"
app.config['UPLOAD_FOLDER'] = "App/upload/"
app.config['DOWNLOAD_FOLDER'] = "App/download/"
app.config['RES_FOLDER'] = "App/res/"

db = SQLAlchemy(app)

import App.views
