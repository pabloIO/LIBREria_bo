import string, random, json, sys, os.path, uuid
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from models import sesion
# import models.models as database
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import func
from sqlalchemy import desc
import uuid
from config.config import env
from werkzeug.utils import secure_filename
from flask import flash, redirect, url_for, jsonify, render_template,send_from_directory, request
from ml_algos import PdfHandler
from models import tables

## Chequear que solo existe una extension
def allowed_file(file, type):
    if type == 'img' and file == None:
        return True
    return '.' in file.filename and \
           file.filename.rsplit('.', 1)[1].lower() in (env['ALLOWED_EXTENSIONS_BOOKS'] if type == 'book' else env['ALLOWED_EXTENSIONS_IMG'])

def id_generator(size=150, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

class UserCtrl(object):
    @staticmethod
    def getBooks(autor_id):
        try:
            res = {
                'success': False,
            }
            autor = tables.AutorIndie.exists(autor_id)
            if not autor:
                return render_template('errors/404.html'), 404
            # book = tables.Libro.get_book(book_id)
            books_body = {
                'books': [ 
                    { 'id': i.li_id,
                    'name': i.li_titulo,
                    'file': i.li_archivo,
                    # 'author': i.autor.complete_name(),
                    # 'likes': i.likes,
                    'downloads': i.li_num_descargas,
                    'views': i.li_numero_vistas,
                    'licencia': i.li_licencia,
                    'image': i.li_imagen } for i in autor.publicacion 
                ]
            }
            res['success'] = True
            res['book'] = books_body
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el Libro, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500

    @staticmethod
    def getAuthor(author_id):
        try:
            res = {
                'success': False,
            }
            author = tables.AutorIndie.exists(author_id)
            # if not user:
            #     return render_template('errors/404.html'), 404
            # book = tables.Libro.get_book(book_id)
            user_body = {
                'id': author.usuario.us_id,
                'name': author.usuario.complete_name(),
                'image': author.usuario.us_foto_perfil,
                'username': author.usuario.us_nombre_usuario,
                'autor': {
                    'id': author.ai_id,
                    'bio': author.ai_biografia,
                    'publications':  author.ai_cantidad_publicaciones
                },
            }
            res['success'] = True
            res['user'] = user_body
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el Libro, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500

    @staticmethod
    def getUser(user_id):
        try:
            res = {
                'success': False,
            }
            user = tables.Usuario.exists_with_id(user_id)
            # if not user:
            #     return render_template('errors/404.html'), 404
            # book = tables.Libro.get_book(book_id)
            user_body = {
                'id': user.us_id,
                'autor': {
                    'id': user.autor[0].ai_id,
                    'bio': user.autor[0].ai_biografia,
                    'publications':  user.autor[0].ai_cantidad_publicaciones
                },
                'name': user.complete_name(),
                'image': user.us_foto_perfil,
                'username': user.us_nombre_usuario,
            }
            res['success'] = True
            res['user'] = user_body
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el Libro, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500

    @staticmethod
    def followingUser(user_id, follower_id):
        try:
            res = {
                'success': False,
            }
            following = tables.AutorSigue.is_following(user_id, follower_id)
            res['success'] = True
            res['following'] = following.as_activo if following else None
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el Libro, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500
    
    @staticmethod
    def followUser():
        try:
            res = {
                'success': False,
            }
            req = request.get_json()
            following = tables.AutorSigue.is_following(req['user_id'], req['followed_id'])
            if not following:
                newfollower = tables.AutorSigue(
                    autor_sigue=req['user_id'],
                    autor_seguido=req['followed_id'],
                )
                newfollower.save()
            else:
                following = tables.AutorSigue.is_following(req['user_id'], req['followed_id'])
                following.as_activo = not req['isFollowing']
                following.save()
            res['follow'] = not req['isFollowing']
            res['success'] = True
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al seguir al autor, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500
    
    @staticmethod
    def getFollowers(author_id):
        try:
            res = {
                'success': False,
            }
            _followers = tables.AutorSigue.get_followers(author_id)
            followers = []
            for follower in _followers:
                if follower.as_activo:
                    followers.append(
                    {    
                        'autor_id': follower.seguido.ai_id,
                        'name': follower.seguido.usuario.complete_name(),
                        'username': follower.seguido.usuario.us_nombre_usuario,
                        'image': follower.seguido.usuario.us_foto_perfil
                    })
            
            res['followers'] = followers
            res['success'] = True
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al seguir al autor, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500

    @staticmethod
    def getFollowing(author_id):
        try:
            res = {
                'success': False,
            }
            _followers = tables.AutorSigue.get_following(author_id)
            followers = []
            for follower in _followers:
                if follower.as_activo:
                    followers.append(
                    {    
                        'autor_id': follower.seguidor.ai_id,
                        'name': follower.seguidor.usuario.complete_name(),
                        'username': follower.seguidor.usuario.us_nombre_usuario,
                        'image': follower.seguidor.usuario.us_foto_perfil
                    })
            
            res['following'] = followers
            res['success'] = True
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al seguir al autor, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500
