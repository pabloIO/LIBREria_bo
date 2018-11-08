from config.config import env
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import uuid
import enum
app = env['APP']
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)
##nota procedimiento almacenado, consulta abajo ...¨
'''
def id_generator(size=150, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Libro(db.Model):
    __tablename__ = 'lb_libro'
    li_id = db.Column(db.Integer, primary_key=True)
    li_titulo = db.Column(db.String(200))
    li_resumen = db.Column(db.Text())
    li_imagen = db.Column(db.String(255))
    li_archivo = db.Column(db.String(255))
    li_num_descargas = db.Column(db.Integer)
    li_idioma = db.Column(db.String(30))
   # li_puntaje_promedio = db.Column(db.float)
    li_numero_vistas = db.Column(db.Integer)
    li_nombre_autor = db.Column(db.String(150))
    li_licencia = db.Column(db.String(45))
    li_activo = db.Column(db.Boolean, nullable=False, default=True)
    li_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    li_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    canal_socket = db.Column(db.String(255))
    li_comments = db.relationship('Comentario')
    #li_like = db.relationship('Like')
    ##########################################################################

class PalabrasClaves(db.Model):
    __tablename__ = 'lb_palabrasclaves'
    pc_id = db.Column(db.Integer, primary_key=True)
    pc_idlibro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    pc_palabra = db.Column(db.String(60))
    pc_tfidf = db.Column(db.Float)
    pc_numero_ocurrencia = db.Column(db.Integer)

class Rol(db.Model):
    __tablename__ = 'lb_rol'
    rl_id = db.Column(db.Integer, primary_key=True)
    rl_descripcion = db.Column(db.String(40), nullable=False)
    rl_abreviation = db.Column(db.String(10))
#################################################################################
class User(db.Model): ##tabla chat -> pendiente...
    __tablename__ = 'lb_usuario'
    us_id = db.Column(db.Integer, primary_key=True)
    #us_idrol = db.Column(db.Integer, db.ForeignKey('lb_rol.id'))
    us_nombre = db.Column(db.String(60), nullable=False)
    us_apellidos = db.Column(db.String(80))
    us_active = db.Column(db.Boolean, nullable=False, default=True)
    us_foto_sperfil = db.Column(db.Text, nullable=True)
    canal_socket = db.Column(db.String(255))
    us_nombre_usuario = db.Column(db.String(50), unique=True)
    us_correo = db.Column(db.String(40), nullable=False)
    us_password = db.Column(db.String(66), nullable=False)
    #facilitar join..
    us_comments = db.relationship('Comentario') #nombre de la clase
    cm_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

'''
'''
class Denuncia(db.Model):
    __tablename__ = 'lb_denuncia' #Libro tiene denuncia
    de_id = db.Column(db.Integer, primary_key=True)
    de_iduser = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'))
    de_idlibro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    de_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    de_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

class AutorIndie(db.Model):
    __tablename__ = 'lb_autorindie' #autor_independiente
    ai_id = db.Column(db.Integer, primary_key=True)
    ai_iduser = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id')) #1 a 1, incluir
    ai_biografia = db.Column(db.Text, nullable=False)
    ai_cantidad_publicaciones = db.Column(db.Integer)
    ai_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ai_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    ai_autorsigue = db.relationship('AutorSigue') #Revisar

class Publicacion(db.Model): ##Revisar
    __tablename__ = 'lb_publicacion'
    pu_id = db.Column(db.Integer, primary_key=True)
    pu_iduserindie = db.Column(db.Integer, nullable=True, db.ForeignKey('lb_autorindie.ai_id'))
    pu_iduser = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'))
    pu_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class AutorSigue(db.Model): ##Revisar.... tabla autor->pendiente...
    __tablename__ = 'lb_autorsigue'
    as_id = db.Column(db.Integer, primary_key=True)
    as_idautorindie = db.Column(db.Integer, db.ForeignKey('lb_autorindie.ai_id'))
    as_idautor = db.Column(db.String(150), db.ForeignKey('lb_libro.li_nombre_autor'))
    as_activo = db.Column(db.Boolean, nullable=False, default=True)
    as_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    as_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

class Genero(db.Model):
    __tablename__ = 'lb_genero'
    ge_id = db.Column(db.Integer, primary_key=True)
    ge_descripcion = db.Column(db.String(50))

class LibroGenero(db.Model):
    __tablename__ = 'lb_librogrenero'
    lg_id = db.Column(db.Integer, primary_key=True)
    lg_idlibro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    lg_idgenero = db.Column(db.Integer, db.ForeignKey('lb_genero.ge_id'))
'''
'''
class Comentario(db.Model):
    __tablename__ = 'lb_comentarios' #libro_tiene_comentario
    cm_id = db.Column(db.Integer, primary_key=True)
    cm_iduser = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'))
    cm_idlibro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    cm_text = db.Column(db.Text())
    cm_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cm_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    '''
'''
class Like(db.Model):
    __tablename__ = 'lb_like' #libro tiene like
    lk_id = db.Column(db.Integer, primary_key=True)
    lk_idlibro = db.Column(db.Integer, db.ForeignKey('lb_libro.li_id'))
    lk_iduser = db.Column(db.Integer, db.ForeignKey('lb_usuario.us_id'))
    lk_puntaje = db.Column(db.Integer)
    lk_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    lk_fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

class Poema(db.Model):
    __tablename__ = 'lb_poema'
    po_id = db.Column(db.Integer, primary_key=True)
    po_verso = db.Column(db.Text)
    po_activo = db.Column(db.Boolean, nullable=False, default=True)
    po_fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    po_fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)
'''
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################
'''
class LicenceType(enum.Enum):
    CREATIVE_COMMONS = 'Creative Commons'
    PUBLIC = 'Dominio público'

class Libro(db.Model):
    __tablename__ = 'libro'
    id = db.Column(db.Integer, primary_key=True)
    nombre_libro = db.Column(db.String(255), nullable=False)
    nombre_archivo = db.Column(db.Text, unique=True, nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    genero = db.Column(db.String(255), nullable=True)
    imagen = db.Column(db.Text, nullable=True)
    likes = db.Column(db.Integer, nullable=False, default=0)
    licencia = db.Column(db.String(50), nullable=False)
    idioma = db.Column(db.String(25), nullable=False, default='Español')
    denuncia_derechos = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ## Define back relation with Conversacion
    comentarios = db.relationship('Comentarios', backref="comentarios", lazy=True)
    ## Define back relation with Sesion
    # sesion = db.relationship('Sesion', backref="sesion", lazy=True)

class Comentarios(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libro.id'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ## Define back relation with Conversacion
    # comentarios = db.relationship('Comentarios', backref="comentarios", lazy=True)
    ## Define back relation with Sesion
    # sesion = db.relationship('Sesion', backref="sesion", lazy=True)

class Poema(db.Model):
    __tablename__ = 'poema'
    id = db.Column(db.Integer, primary_key=True)
    verso = db.Column(db.Text, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

db.create_all()
'''
####Ej:-Procedimiento almacenado...//.Ejecutar como consulta sql
'''
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from lb_user where us_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into lb_user
        (
            us_name,
            us_username,
            us_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;
'''