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
from ml_algos import PdfHandler, CommentHandler, CsvHandler
from models import tables
import datetime
import numpy as np
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

class LibrosCtrl(object):
    @staticmethod
    def all(page_num):
        try:
            res = {
                'success': False,
            }
            total = tables.Libro.query.filter(tables.Libro.li_activo == True)
            books = tables.Libro.activeBooks(page_num)
            if books == None:
                res['books'] = []
            else:
                # print(books.comentarios)
                serialized = [ { 'id': i.li_id,
                                'name': i.li_titulo,
                                'file': i.li_archivo,
                                # 'likes': i.likes,
                                'licencia': i.li_licencia,
                                'autor': tables.Libro.getAuthor(i.li_id),
                                'image': i.li_imagen } for i in books ]
                res['books'] = serialized
            res['success'] = True
            res['total'] = get_count(total)
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al obtener los tables.Libros, inténtelo nuevamente'
        finally:
            resp = jsonify(res)
            return resp, 200
            
    @staticmethod
    def getBook(book_id):
        try:
            res = {
                'success': False,
            }
            book = tables.Libro.exists(book_id)
            if not book:
                return render_template('errors/404.html'), 404
            # book = tables.Libro.get_book(book_id)
            book.update_num_views()
            book_body = {
                'id': book.li_id,
                'keywords': [
                    {
                        'text': word.pc_palabra,
                        'weight': word.pc_ocurrencia
                    } for word in book.palabras_clave
                ],
                'title': book.li_titulo,
                'image': book.li_imagen,
                'downloads': book.li_num_descargas,
                'file': book.li_archivo,
                'language': book.li_idioma,
                'created_at': datetime.datetime.strftime(book.li_fecha_creacion, '%Y-%m-%d'),
                'comments': [
                    {
                        'text': comment.cm_texto,
                        'date': comment.cm_fecha_creacion,
                        'autor': comment.autor.usuario.complete_name(),
                        'username': comment.autor.usuario.us_nombre_usuario,
                        'autor_id': comment.autor.ai_id,
                    } for comment in book.comentarios
                ],
                'genre': [
                    {
                        'id': word.ge_id,
                        'desc': word.ge_descripcion,
                    } for word in book.generos
                ],
            }
            res['success'] = True
            res['book'] = book_body
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el Libro, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500

    @staticmethod
    def getBookStatistics(book_id):
        try:
            res = {
                'success': False,
            }
            book = tables.Libro.exists(book_id)
            if not book:
                return render_template('errors/404.html'), 404
            # book = tables.Libro.get_book(book_id)
            book_body = {
                'id': book.li_id,
                'keywords': [
                    {
                        'text': word.pc_palabra,
                        'weight': word.pc_ocurrencia
                    } for word in book.palabras_clave
                ],
                'comments': [
                    {
                        'text': comment.cm_texto,
                        'date': comment.cm_fecha_creacion,
                        'autor': comment.autor.usuario.complete_name(),
                        'username': comment.autor.usuario.us_nombre_usuario,
                        'autor_id': comment.autor.ai_id,
                    } for comment in book.comentarios
                ],
                'title': book.li_titulo,
                'image': book.li_imagen,
                'downloads': book.li_num_descargas,
                'views': book.li_numero_vistas,
                'file': book.li_archivo,
                'language': book.li_idioma,
                'genre': [
                    {
                        'id': word.ge_id,
                        'desc': word.ge_descripcion,
                    } for word in book.generos
                ],
            }
            commentTf = CommentHandler.CommentHandler('es', book_body['comments'])
            res['success'] = True
            res['book'] = book_body
            res['comment_wc'] = [{'text': word[0], 'weight': word[1]} for word in commentTf.get_word_cloud(0.5)]
            resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el Libro, inténtelo nuevamente'
            resp = jsonify(res)
            return resp, 500

    @staticmethod
    def getBooksStatistics(autor_id):
        try:
            res = {
                'success': False,
            }
            autor = tables.AutorIndie.exists(autor_id)
            if not autor:
                return render_template('errors/404.html'), 404
            books = autor.publicacion
            report_body = [
                {
                    'id': book.li_id,
                    'title': book.li_titulo,
                    'image': book.li_imagen,
                    'downloads': book.li_num_descargas,
                    'views': book.li_numero_vistas,
                    'likes': int(np.sum([ like.lk_puntaje for like in book.likes ]))
                }
                for book in books
            ]
            keywords = []
            for book in books:
                _keywords = [ {'text': keyword.pc_palabra, 'weight': keyword.pc_ocurrencia } for keyword in book.palabras_clave ]
                keywords.extend(_keywords)
            res['word_cloud_keywords'] = keywords
            res['success'] = True
            res['books'] = report_body
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
    def denounceBook(book_id):
        try:
            res = {
                'success': False,
            }
            req = request.get_json()
            print(req)
            denounce = tables.Denuncias(
                de_descripcion=req['desc'],
                autor_id=req['autor_id'],
                libro_id=book_id
            )
            print(denounce)
            denounce.save()
            res['success'] = True
            res['msg'] = 'El libro acaba de ser denunciado, revisaremos su solicitud para tomar las acciones pertinentes, gracias'
            return jsonify(res), 200
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al procesar su solicitud, inténtelo nuevamente'
            return jsonify(res), 500
        
    @staticmethod
    def rateBook(book_id):
        try:
            res = {
                'success': False,
            }
            req = request.get_json()
            rate = tables.Like.exists(req['autor_id'], book_id)
            if not rate:
                like = tables.Like(
                    autor_id=req['autor_id'],
                    libro_id=book_id,
                    lk_puntaje=req['rating']
                )
                like.save()
            else:
                rate.lk_puntaje = req['rating']
                rate.save()
            res['success'] = True
            res['msg'] = 'Se agrego su puntuación'
            return jsonify(res), 200
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al agregar su puntuacion'
            return jsonify(res), 500

    @staticmethod
    def getRating(book_id, autor_id):
        try:
            res = {
                'success': False,
            }
            rate = tables.Like.exists(autor_id, book_id)
            res['rating'] = rate.lk_puntaje if rate else 0
            res['success'] = True
            res['msg'] = 'Se agrego su puntuación'
            return jsonify(res), 200
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al agregar su puntuacion'
            return jsonify(res), 500

    @staticmethod
    def uploadBook(db, request, response):
        try:
            res = {
                'success': False,
            }
            if request.method == 'POST':
                if 'filebook' not in request.files:
                    res['success'] = False
                    res['msg'] = 'Debe seleccionar un archivo del escrito'
                    res['code'] = 400
                bookfile = request.files['filebook']
                imgfile = request.files['fileimg'] if 'fileimg' in request.files else None
                if bookfile.filename == '':
                    res['success'] = False
                    res['msg'] = 'Debe seleccionar un archivo del escrito'
                    res['code'] = 400
                if (bookfile and allowed_file(bookfile, 'book')) and (imgfile or allowed_file(imgfile, 'img')):
                    bookfilename = uuid.uuid4().hex + secure_filename(bookfile.filename)
                    imgfilename = uuid.uuid4().hex + secure_filename(imgfile.filename) if imgfile else None
                    autor = tables.AutorIndie.exists(request.form['autor_id'])
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
                    word_cloud, df = pdfHandler.get_word_cloud(0.15)
                    # csv = CsvHandler.CsvHandler(bookfilename.replace('.pdf', '.csv'))
                    # newBook.li_keywords_csv = csv_file
                    newBook.saveKeyWords(word_cloud)
                    # tables.Libro.save(newBook)
                    newBook.save()
                    if imgfilename != None: imgfile.save(os.path.join(env['UPLOADS_DIR'] + '/images', imgfilename))
                    res['success'] = True
                    res['route'] = 'libro-exito'
                    res['book_id'] = newBook.li_id
                else:
                    print('err')
                    res['success'] = False
                    res['msg'] = 'Formato no aceptado'
                    res['code'] = 400
                resp = jsonify(res)
                return resp, 200
        except Exception as e:
            db.session.rollback()
            res['route'] = 'libro-error'
            resp = jsonify(res)
            return resp, 500

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

    @staticmethod
    def commentBook():
        res = { 'success': False }
        try:
            req = request.get_json()
            book = tables.Libro.exists(req['book_id'])
            if not book:
                return render_template('errors/404.html'), 404
            comment = tables.Comentario(
                libro_id=req['book_id'],
                autor_id=req['autor_id'],
                cm_texto=req['text'],
            )
            book.comentarios.append(comment)
            book.save()
            res['success'] = True
            res['comment'] = {
                'text': comment.cm_texto,
                'date': comment.cm_fecha_creacion,
                'autor': comment.autor.usuario.complete_name(),
                'username': comment.autor.usuario.us_nombre_usuario,
                'autor_id': comment.autor.ai_id,
            } 
            # res['downloads_counter'] = book.li_num_descargas
            return jsonify(res), 200
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al actualizar el contador de descargas'
            return jsonify(res), 200