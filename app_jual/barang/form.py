from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField,SelectField
from wtforms.validators import DataRequired

jenis = [
    ('Rokok','Rokok'),
    ('Sembako','Sembako'),
]

class BarangForm(FlaskForm):
    nama_barang = StringField('Nama',validators=[DataRequired()])
    harga = FloatField('Harga',validators=[DataRequired()])
    qt = FloatField('Qt',validators=[DataRequired()])
    jenis = SelectField("Jenis",choices=jenis,validators=[DataRequired()]\
        , default=jenis[0][0])
    submit = SubmitField('Simpan')
