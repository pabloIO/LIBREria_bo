import os
from app import db
from config.config import env
from datetime import datetime
import string
import random
import uuid
import enum
from werkzeug import generate_password_hash, check_password_hash

class Usuario(db.Model): ##tabla chat -> pendiente...
    __tablename__ = 'lb_usuario'
    us_id = db.Column(db.Integer, primary_key=True)
    #us_idrol = db.Column(db.Integer, db.ForeignKey('lb_rol.id'))
    us_nombre = db.Column(db.String(60), nullable=False)
    us_apellidos = db.Column(db.String(80))
    us_active = db.Column(db.Boolean, nullable=False, default=True)
    us_foto_sperfil = db.Column(db.Text, nullable=True)
    us_canal_socket = db.Column(db.String(255))
    us_nombre_usuario = db.Column(db.String(50), unique=True)
    us_correo = db.Column(db.String(40), nullable=False)
    us_password = db.Column(db.String(66), nullable=False)
    us_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    us_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    li_rol = db.relationship('Rol', backref="lb_usuario", lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, email):
        return cls.query.filter_by(us_correo = email).first()

    @staticmethod
    def check_password(plain_password, db_password):
        return check_password_hash(plain_password, db_password)
    #facilitar join..
    # us_comments = db.relationship('Comentario') #nombre de la clase
    # cm_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Libro(db.Model):
    __tablename__ = 'lb_libro'
    li_id = db.Column(db.Integer, primary_key=True)
    li_titulo = db.Column(db.String(200))
    li_resumen = db.Column(db.Text())
    li_imagen = db.Column(db.String(255))
    li_archivo = db.Column(db.String(255))
    li_num_descargas = db.Column(db.Integer)
    li_idioma = db.Column(db.String(30))
    li_numero_vistas = db.Column(db.Integer)
    li_nombre_autor = db.Column(db.String(150))
    li_licencia = db.Column(db.String(45))
    li_activo = db.Column(db.Boolean, nullable=False, default=True)
    li_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    li_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    li_canal_socket = db.Column(db.String(255))
    #     ## Define back relation with Conversacion
    li_comentarios = db.relationship('Comentario', backref="lb_libro", lazy=True)
    li_palabras_clave = db.relationship('PalabrasClave', backref="lb_libro", lazy=True)
    li_denuncias = db.relationship('Denuncia', backref="lb_libro", lazy=True)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class Comentario(db.Model):
    __tablename__ = 'lb_comentarios' 
    cm_id = db.Column(db.Integer, primary_key=True)
    cm_id_usuario = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'), nullable=False)
    cm_id_libro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'), nullable=False)
    cm_texto = db.Column(db.Text(), nullable=False)
    cm_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cm_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

class PalabrasClaves(db.Model):
    __tablename__ = 'lb_palabras_claves'
    pc_id = db.Column(db.Integer, primary_key=True)
    pc_id_libro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    pc_palabra = db.Column(db.String(60))
    # pc_count_word = db.Column(db.Float)
    pc_ocurrencia = db.Column(db.Float)

    @classmethod
    def save(cls, words):
        db.engine.execute(cls.__table__.insert(), words)

class Denuncia(db.Model):
    __tablename__ = 'lb_denuncia' #Libro tiene denuncia
    de_id = db.Column(db.Integer, primary_key=True)
    de_id_usuario = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'))
    de_id_libro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    de_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    de_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

class Genero(db.Model):
    __tablename__ = 'lb_genero'
    ge_id = db.Column(db.Integer, primary_key=True)
    ge_descripcion = db.Column(db.String(50))

generos =  db.Table('lb_libro_genero',
    db.Column('lg_id', db.Integer, primary_key=True),
    db.Column('lg_libro_id', db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('lg_usuario_id',  db.Integer, db.ForeignKey('lb_genero.ge_id'), primary_key=True)
)

likes = db.Table('lb_like', #libro tiene like
    db.Column( 'lk_id', db.Integer, primary_key=True),
    db.Column('lk_libro_id',  db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('lk_usuario_id', db.Integer, db.ForeignKey('lb_usuario.us_id'), primary_key=True),
    db.Column('lk_puntaje' , (db.Integer), default=0),
    db.Column('lk_fecha_creacion', db.DateTime, default=datetime.utcnow),
    db.Column('lk_fecha_actualizacion', db.DateTime, default=datetime.utcnow)
)

class Rol(db.Model):
    __tablename__ = 'lb_rol'
    rl_id = db.Column(db.Integer, primary_key=True)
    rl_descripcion = db.Column(db.String(40), nullable=False)
    rl_abreviation = db.Column(db.String(10))
#################################################################################

class AutorIndie(db.Model):
    __tablename__ = 'lb_autor_indie' #autor_independiente
    ai_id = db.Column(db.Integer, primary_key=True)
    ai_id_usuario = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id')) #1 a 1, incluir
    ai_biografia = db.Column(db.Text, nullable=False)
    ai_cantidad_publicaciones = db.Column(db.Integer)
    ai_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ai_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    ai_autor_sigue = db.relationship('AutorSigue', backref='lb_autor_indie', lazy=True) #Revisar

class AutorSigue(db.Model): ##Revisar.... tabla autor->pendiente...
    __tablename__ = 'lb_autorsigue'
    as_id = db.Column(db.Integer, primary_key=True)
    as_id_autor_sigue = db.Column(db.Integer, db.ForeignKey('lb_autor_indie.ai_id'))
    as_id_autor_seguido = db.Column(db.Integer, db.ForeignKey('lb_autor_indie.ai_id'))
    as_activo = db.Column(db.Boolean, nullable=False, default=True)
    as_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    as_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

####Ej:-Procedimiento almacenado...//.Ejecutar como consulta sql
'''
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createusuario`(
    IN p_name VARCHAR(20),
    IN p_usuarioname VARCHAR(20),
    IN p_password VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from lb_usuario where us_usuarioname = p_usuarioname) ) THEN
     
        select 'usuarioname Exists !!';
     
    ELSE
     
        insert into lb_usuario
        (
            us_name,
            us_usuarioname,
            us_password
        )
        values
        (
            p_name,
            p_usuarioname,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;
'''