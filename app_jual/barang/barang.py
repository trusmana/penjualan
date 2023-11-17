from flask import Flask, render_template,Blueprint,redirect,\
    flash,url_for,request,session
from app_jual.models import Barang
from app_jual import db,socketio
from app_jual.barang import form as fm

# Untuk mengatur Aplikasi Flask Menjadi Struktur yg modular
blprint = Blueprint('barang',__name__)

@blprint.route('/barang')
def list_barang():
    user_email = session.get('email','Pengunjung')
    barangs = Barang.query.all()
    return render_template('barang/barang.html',barangs=barangs,user_email=user_email)

@blprint.route("/barang/add",methods=['POST','GET'])
def add():
    user_email = session.get('email','Pengunjung')
    form = fm.BarangForm()
    if form.validate_on_submit():
        nama_barang = form.nama_barang.data
        harga = form.harga.data
        qt = form.qt.data
        jenis = form.jenis.data
        new_barang = Barang(nama_barang=nama_barang,harga=harga,\
            qt=qt,jenis=jenis)
        db.session.add(new_barang)
        db.session.commit()

        socketio.emit("data_added",{
            'id': new_barang.id,
            'nama_barang': new_barang.nama_barang,
            'harga': new_barang.harga,
            'jenis': new_barang.jenis,
            'qt': new_barang.qt,
        })

        flash('Data berhasil Disimpan', 'success')
        return redirect(url_for('barang.list_barang'))
    return render_template('barang/add_barang.html',form=form,user_email=user_email)

@blprint.route("/barang/edit/<int:id>",methods=['POST','GET'])
def edit(id):
    barang = Barang.query.get(id)
    form = fm.BarangForm(obj=barang)
    if request.method =='POST' and form.validate_on_submit:
        form.populate_obj(barang)
        db.session.commit()
        flash('Data Berhasil Di edit','succces')
        return redirect(url_for('barang.list_barang'))
    return render_template('barang/edit_barang.html',barang= barang,\
        form=form)

@blprint.route("/barang/delete/<int:id>")
def delete(id):
    barang = Barang.query.get(id)
    db.session.delete(barang)
    db.session.commit()
    flash('Data Berhasil Di Hapus','succces')
    return redirect(url_for('barang.list_barang'))