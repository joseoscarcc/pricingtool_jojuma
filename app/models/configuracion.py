from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from app.extensions import db

class UserDataForm(FlaskForm):
    user = StringField('usuario', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    amount = IntegerField('Amount', validators = [DataRequired()])                                   
    submit = SubmitField('Generate Report')

class marcas_places(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    cre_id = db.Column(db.Text)
    brand = db.Column(db.Text)
    cp = db.Column(db.Text)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    es_norte = db.Column(db.Text)
    municipio = db.Column(db.Text)
    estado = db.Column(db.Text)
    terminal = db.Column(db.Text)
    brand_2 = db.Column(db.Text)
    