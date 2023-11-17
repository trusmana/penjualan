from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#### adalah Librery Javascript yang maungkinkan komunikasi real-time
#### anatara clien dan server
from flask_socketio import SocketIO

app= Flask(__name__)

socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///penjualan.db'
csrf = CSRFProtect(app)
db =SQLAlchemy(app)
app.secret_key='qwert'

from app_jual.barang.barang import blprint
app.register_blueprint(blprint)
