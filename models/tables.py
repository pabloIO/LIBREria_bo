import os
from app import db
from config.config import env
from datetime import datetime
import string
import random
import uuid
import enum
from passlib.hash import pbkdf2_sha256
from sqlalchemy import desc
publicacion = db.Table('lb_autor_publica', #libro tiene like
    # db.Column('au_pub_id', db.Integer, primary_key=True, default = uuid.uuid4() ),
    db.Column('libro_id',  db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('autor_id', db.Integer, db.ForeignKey('lb_autor_indie.ai_id'), primary_key=True),
    db.Column('au_pub_fecha_creacion', db.DateTime, default=datetime.utcnow),
    db.Column('au_pub_fecha_actualizacion', db.DateTime, default=datetime.utcnow)
)

libro_comentario = db.Table('lb_libro_comentarios',
    db.Column('cm_id', db.Integer, primary_key=True),
    db.Column('libro_id',  db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('autor_id', db.Integer, db.ForeignKey('lb_autor_indie.ai_id'), primary_key=True),
    db.Column('cm_texto', db.Text, nullable=False),
    db.Column('cm_fecha_creacion', db.DateTime, default=datetime.utcnow),
    db.Column('cm_fecha_actualizacion', db.DateTime, default=datetime.utcnow)
)

generos =  db.Table('lb_libro_genero',
    db.Column('lg_id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('libro_id', db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('genero_id',  db.Integer, db.ForeignKey('lb_genero.ge_id'), primary_key=True),
    db.Column('lk_fecha_creacion', db.DateTime, default=datetime.utcnow),
    db.Column('lk_fecha_actualizacion', db.DateTime, default=datetime.utcnow)
)

likes = db.Table('lb_like', #libro tiene like
    db.Column('lk_id', db.Integer, primary_key=True),
    db.Column('libro_id',  db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('autor_id', db.Integer, db.ForeignKey('lb_autor_indie.ai_id'), primary_key=True),
    db.Column('lk_puntaje' , (db.Integer), default=0),
    db.Column('lk_fecha_creacion', db.DateTime, default=datetime.utcnow),
    db.Column('lk_fecha_actualizacion', db.DateTime, default=datetime.utcnow)
)

denuncias = db.Table('lb_denuncias',
    db.Column('de_id', db.Integer, primary_key=True),
    db.Column('libro_id',  db.Integer, db.ForeignKey('lb_libro.li_id'), primary_key=True),
    db.Column('autor_id',  db.Integer, db.ForeignKey('lb_autor_indie.ai_id'), primary_key=True),
    db.Column('de_descripcion', db.Text, nullable=False),
    db.Column('de_fecha_creacion', db.DateTime, default=datetime.utcnow),
    db.Column('de_fecha_actualizacion', db.DateTime, default=datetime.utcnow)
)

class Usuario(db.Model): ##tabla chat -> pendiente...
    __tablename__ = 'lb_usuario'
    us_id = db.Column(db.Integer, primary_key=True)
    #us_idrol = db.Column(db.Integer, db.ForeignKey('lb_rol.id'))
    us_nombre = db.Column(db.String(60), nullable=False)
    us_apellidos = db.Column(db.String(80))
    us_active = db.Column(db.Boolean, nullable=False, default=True)
    us_foto_perfil = db.Column(db.Text, nullable=True)
    us_canal_socket = db.Column(db.String(255), nullable=False, default=uuid.uuid4().hex)
    us_nombre_usuario = db.Column(db.String(50), unique=True)
    us_correo = db.Column(db.String(40), nullable=False)
    us_password = db.Column(db.String(255), nullable=False)
    us_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    us_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    rol_id = db.Column(db.Integer, db.ForeignKey("lb_rol.rl_id"), nullable=False)
    autor = db.relationship('AutorIndie', backref="lb_usuario", lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def exists(cls, email):
        return cls.query.filter_by(us_correo = email).first()

    @classmethod
    def exists_with_id(cls, id):
        return cls.query.filter_by(us_id = id).first()

    @staticmethod
    def hash_password(plain):
        return pbkdf2_sha256.hash(plain) 

    @staticmethod
    def check_password(plain_password, hashed):
        return pbkdf2_sha256.verify(plain_password, hashed)

    def complete_name(self):
        return '{0} {1}'.format(self.us_nombre, self.us_apellidos)
    #facilitar join..
    # us_comments = db.relationship('Comentario') #nombre de la clase
    # cm_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class PalabrasClave(db.Model):
    __tablename__ = 'lb_palabras_claves'
    pc_id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'), nullable=False)
    pc_palabra = db.Column(db.Text)
    # pc_count_word = db.Column(db.Float)
    pc_ocurrencia = db.Column(db.Float)
    pc_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    pc_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self, words):
        try:
            ## subir para palabra clave
            pass
        except Exception as e:
            pass

class Libro(db.Model):
    __tablename__ = 'lb_libro'
    li_id = db.Column(db.Integer, primary_key=True)
    li_titulo = db.Column(db.String(255), nullable=False)
    li_resumen = db.Column(db.Text, nullable=True)
    li_imagen = db.Column(db.String(255), nullable=True)
    li_archivo = db.Column(db.String(255), nullable=False)
    li_num_descargas = db.Column(db.Integer, nullable=False, default=0)
    li_idioma = db.Column(db.String(30), nullable=False)
    li_numero_vistas = db.Column(db.Integer, nullable=False, default=0)
    # li_nombre_autor = db.Column(db.String(150))
    li_licencia = db.Column(db.String(45), nullable=False)
    li_activo = db.Column(db.Boolean, nullable=False, default=True)
    li_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    li_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    li_canal_socket = db.Column(db.String(255), nullable=False, default=uuid.uuid4().hex)
    #     ## Define back relation with Conversacion
    # autor = db.relationship('AutorIndie', secondary=publicacion, backref=db.backref('lb_libro', lazy='dynamic'))
    comentarios = db.relationship('AutorIndie', secondary=libro_comentario, backref=db.backref('lb_libro', lazy='dynamic'))
    generos = db.relationship('Genero', secondary=generos, backref=db.backref('lb_libro', lazy='dynamic'))
    palabras_clave = db.relationship('PalabrasClave', backref="lb_libro", lazy=True)
    # li_denuncias = db.relationship('Denuncia', secondary=denuncias, lazy="subquery", backref="lb_libro")
    # denuncias = db.relationship('AutorIndie', secondary=denuncias, foreign_keys=[''],  backref=db.backref('lb_libro', lazy='dynamic'))
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def exists(cls, id):
        return cls.query.filter_by(li_id = id).first()

    @classmethod
    def get_book(cls, id):
        return cls.query.get(li_id = book_id)

    def update_num_views(self):
        self.li_numero_vistas = self.li_numero_vistas + 1
        db.session.commit()

    def update_num_downloads(self):
        self.li_num_descargas = self.li_num_descargas + 1
        db.session.commit()

    def saveKeyWords(self, words):
        for word in words:
            word = PalabrasClave(
                pc_palabra=word[0],
                pc_ocurrencia=word[1],
            )
            self.palabras_clave.append(word)
    
    @classmethod
    def activeBooks(cls, page_num):
        return cls.query.filter(cls.li_activo == 1) \
                    .order_by(desc(cls.li_id)) \
                    .paginate(page=int(page_num), per_page=24) \
                    .items

class Genero(db.Model):
    __tablename__ = 'lb_genero'
    ge_id = db.Column(db.Integer, primary_key=True)
    ge_descripcion = db.Column(db.String(50))

class Rol(db.Model):
    __tablename__ = 'lb_rol'
    rl_id = db.Column(db.Integer, primary_key=True)
    rl_descripcion = db.Column(db.String(40), nullable=False)
    rl_abreviation = db.Column(db.String(10))
#################################################################################

class AutorIndie(db.Model):
    __tablename__ = 'lb_autor_indie' #autor_independiente
    ai_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id')) #1 a 1, incluir
    ai_biografia = db.Column(db.Text, nullable=True)
    ai_cantidad_publicaciones = db.Column(db.Integer, nullable=True, default=0)
    ai_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ai_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    publicacion = db.relationship('Libro', secondary=publicacion, backref=db.backref('lb_autor_indie', lazy='dynamic'))
    # ai_autor_sigue = db.relationship('AutorSigue', backref='lb_autor_indie', lazy=True) #Revisar
    
    def save(self):
        db.session.add(self)    
        db.session.commit()  
    @classmethod
    def exists(cls, aid):
        return cls.query.filter_by(ai_id = aid).first()  

class AutorSigue(db.Model): ##Revisar.... tabla autor->pendiente...
    __tablename__ = 'lb_autor_sigue'
    as_id = db.Column(db.Integer, primary_key=True)
    autor_sigue = db.Column(db.Integer, db.ForeignKey('lb_autor_indie.ai_id'))
    autor_seguido = db.Column(db.Integer, db.ForeignKey('lb_autor_indie.ai_id'))
    as_activo = db.Column(db.Boolean, nullable=False, default=True)
    as_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    as_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

# class Comentario(db.Model):
#     __tablename__ = 'lb_comentarios' 
#     cm_id = db.Column(db.Integer, primary_key=True)
#     cm_id_usuario = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'), nullable=False)
#     cm_id_libro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'), nullable=False)
#     cm_texto = db.Column(db.Text(), nullable=False)
#     cm_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
#     cm_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)


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