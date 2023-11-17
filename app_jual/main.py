from flask import render_template,redirect,\
    session,url_for,flash
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from app_jual import app,db,socketio
from app_jual.forms import RegisterForm,LoginForm
from app_jual.models import User


@app.route("/")
def home():
    user_email = session.get('email','Pengunjung')
    aplikasi = ['Beras', 'Gula', 'Minyak', 'Terigu','Rokok']
    nilainya = [95, 80, 65 ,80,50]
    eksplorasi =[0,0,0.1,0,0]
    plt.pie(nilainya, labels=aplikasi,explode=eksplorasi, autopct='%1.1f%%')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('index.html',plot_url=plot_url,user_email=user_email)

@app.route("/register",methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nama = form.nama.data
        email = form.email.data
        password = form.password.data
        ### Menu Cek data Apakah User Sudah Terdaftar
        exist_user = User.query.filter_by(email=email).first()
        if exist_user:
            flash('User yang Ada Masukan Terdaftar','danger')
            return redirect(url_for("register"))
        ###menu Buat User Baru
        new_user = User(nama=nama,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Pendaftaran User Berhasil','success')
        return redirect(url_for('login'))

    return render_template('auth/register.html',form=form)

@app.route("/login",methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password= form.password.data
        pengguna = User.query.filter_by(email=email).first()
        if pengguna and pengguna.check_password(password=password):
            session['email'] =pengguna.email
            flash('Login Berhasih','success')
            return redirect(url_for('home'))
        else:
            flash('Login Gagal. Perikasa email atau Password anda','danger')
            return redirect(url_for('login'))

    return render_template('auth/login.html',form=form)

@app.route("/logout")
def logout():
    ##hapus email dari sesi logout
    session.clear()
    flash('Anda telah Berhasil Logout','success')
    return redirect(url_for('home'))

@socketio.on('message')
def handle_message(msg):
    socketio.emit('message',msg)