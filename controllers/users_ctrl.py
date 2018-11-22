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
from flask import flash, redirect, url_for, jsonify, render_template,send_from_directory
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
    def searchBook(query_p, db, response):
        try:
            res = {
                'success': False,
            }
            books = tables.Libro.query.filter(
                        tables.Libro.autor.like('%{}%'.format(query_p)) |
                        tables.Libro.nombre_tables.Libro.like('%{}%'.format(query_p)),
                        tables.Libro.activo == 1
                    ).all()
            if books == None:
                res['books'] = []
            else:
                # print(books.comentarios)
                serialized = [ { 'id': i.id,
                                'name': i.nombre_tables.Libro,
                                'file': i.nombre_archivo,
                                'author': i.autor,
                                'likes': i.likes,
                                'licencia': i.licencia,
                                'image': i.imagen } for i in books ]
                res['books'] = serialized

            res['success'] = True
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el tables.Libro, inténtelo nuevamente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

    @staticmethod
    def denounceBook(db, request, response):
        try:
            res = {
                'success': False,
            }
            book = tables.Libro.query.get(request.form['id'])
            book.denuncia_derechos = request.form['desc']
            book.activo = False
            db.session.commit()
            res['success'] = True
            res['msg'] = 'El tables.Libro que subió acaba de ser denunciado, revisaremos su solicitud, por el momento ha sido dado de baja de la LIBREria, recargue la página para ver los cambios'
        except Exception as e:
            print(e)
            db.session.rollback()
            res['msg'] = 'Hubo un error al procesar su solicitud, inténtelo nuevamente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

    @staticmethod
    def uploadBook(db, request, response):
        try:
            res = {
                'success': False,
            }
            if request.method == 'POST':
                # print(request.files['fileimg'] == None)
                if 'filebook' not in request.files:
                    res['success'] = False
                    res['msg'] = 'Debe seleccionar un archivo del escrito'
                    res['code'] = 400
                bookfile = request.files['filebook']
                print('subiendo book')
                imgfile = request.files['fileimg'] if 'fileimg' in request.files else None
                if bookfile.filename == '':
                    res['success'] = False
                    res['msg'] = 'Debe seleccionar un archivo del escrito'
                    res['code'] = 400
                if (bookfile and allowed_file(bookfile, 'book')) and (imgfile or allowed_file(imgfile, 'img')):
                    bookfilename = uuid.uuid4().hex + secure_filename(bookfile.filename)
                    imgfilename = uuid.uuid4().hex + secure_filename(imgfile.filename) if imgfile else None
                    print(imgfilename)
                    print(bookfilename)
                    autor = tables.AutorIndie.find(request.form['autor_id'])
                    newBook = tables.Libro(
                        li_titulo=request.form['book'],
                        li_idioma=request.form['language'],
                        li_licencia=request.form['licence'],
                        li_archivo=bookfilename,
                        li_imagen=imgfilename,
                    )
                    autor.publicacion.append(newBook)
                    tables.AutorIndie.save(autor)
                    # db.session.add(autor)
                    genero = tables.Genero(ge_descripcion = request.form['genre'])
                    newBook.generos.append(genero)
                    path_book = os.path.join(env['UPLOADS_DIR'] + '/books', bookfilename)
                    bookfile.save(path_book)
                    pdfHandler = PdfHandler.PdfHandler(request.form['language'], path_book)
                    # pdfHandler = PdfHandler(request.form['language'])
                    word_cloud = pdfHandler.get_word_cloud(0.15)
                    newBook.saveKeyWords(word_cloud)
                    tables.Libro.save(newBook)

                    if imgfilename != None: imgfile.save(os.path.join(env['UPLOADS_DIR'] + '/images', imgfilename))
                    
                    res['success'] = True
                    return
                    res['route'] = 'libro-exito'
                else:
                    print('err')
                    res['success'] = False
                    res['msg'] = 'Formato no aceptado'
                    res['code'] = 400
            else:
                res['success'] = True
                res['route'] = 'tables.Libro-exito'
        except Exception as e:
            print(e)
            db.session.rollback()
            res['route'] = 'tables.Libro-error'
        finally:
            return response(json.dumps(res), mimetype='application/json')
    @staticmethod
    def downloadBook(book_id):
        res = { 'success': False }
        try:
            book = tables.Libro.exists(book_id)
            if not book:
                return render_template('errors/404.html'), 404
            book.update_num_downloads()
            res['success'] = True
            res['downloads_counter'] = book.li_num_descargas
            return jsonify(res), 200
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al actualizar el contador de descargas'
            return jsonify(res), 200