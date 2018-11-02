from config.config import env
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import uuid
app = env['APP']
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)
            
def id_generator(size=150, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(45), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _conversation_id = db.Column(db.String(255), nullable=False)
    canal_socket = db.Column(db.String(255), nullable=False, default=id_generator())
    ## Define back relation with Conversacion
    conversaciones = db.relationship('Conversacion', backref="conversacion", lazy=True)
    ## Define back relation with Sesion
    sesion = db.relationship('Sesion', backref="sesion", lazy=True)

# class Sesion(db.Model):
#     __tablename__ = 'sesion'
#     id = db.Column(db.Integer, primary_key=True)
#     token = db.Column(db.Text, nullable=False, default=uuid.uuid4().hex)
#     fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     ### FK from table usuarios
#     usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
#     # usuarios = db.relationship('Usuarios',  backref=db.backref('sesion', lazy=True))

# class Conversacion(db.Model):
#     '''
#     Atribs from the table
#     '''
#     __tablename__ = 'conversacion'
#     __table_args__ = {'schema': config['SQL_CONF']['DB_NAME']}
#     id = db.Column(db.Integer, primary_key=True)
#     texto = db.Column(db.Text, nullable=False)
#     fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     ### FK FROM TABLE SESSION
#     sesion_id = db.Column(Integer, db.ForeignKey('sesion.id'), nullable=False)
#     sesion = db.relationship('Sesion', backref=db.backref('conversacion', lazy=True))

#     ### FK from table usuarios
#     usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
#     usuarios = db.relationship('Usuarios',  backref=db.backref('usuarios', lazy=True))
    


# db.create_all()

