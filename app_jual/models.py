from app_jual import app,db
from enum import Enum
import bcrypt


class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nama = db.Column(db.String(100),nullable=True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,nama):
        self.email =email
        self.nama=nama
        self.password=bcrypt.hashpw(password.encode('utf-8'),\
            bcrypt.gensalt()).decode('utf-8')
        
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),\
            self.password.encode('utf-8'))
    
class Barang(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nama_barang = db.Column(db.String(100),nullable=True)
    harga = db.Column(db.Float,nullable=True)
    qt = db.Column(db.Float,nullable=True)
    jenis = db.Column(db.String(1))

with app.app_context():
    db.create_all()