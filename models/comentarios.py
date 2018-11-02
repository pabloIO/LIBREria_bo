from config.config import env
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import uuid
app = env['APP']
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)

class Comentarios(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ## Define back relation with Libro
    sesion = db.relationship('Libro', backref=db.backref('libro', lazy=True))
    ## Define back relation with Sesion
    # sesion = db.relationship('Sesion', backref="sesion", lazy=True)
