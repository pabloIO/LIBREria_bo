import string, random, json, sys, os.path, uuid
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from models import sesion
import models.models as database
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import func
from sqlalchemy import desc
import uuid
from config.config import env
from werkzeug.utils import secure_filename
from flask import flash, redirect, url_for, jsonify
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
    def all(page_num, db, response):
        try:
            res = {
                'success': False,
            }
            total = database.Libro.query.filter(database.Libro.activo == 1)
            books = database.Libro.query.filter(database.Libro.activo == 1).order_by(desc(database.Libro.id)).paginate(page=int(page_num), per_page=24).items
            print(books)
            if books == None:
                res['books'] = []
            else:
                # print(books.comentarios)
                serialized = [ { 'id': i.id,
                                'name': i.nombre_libro,
                                'file': i.nombre_archivo,
                                'author': i.autor,
                                'likes': i.likes,
                                'licencia': i.licencia,
                                'image': i.imagen } for i in books ]
                res['books'] = serialized
            res['success'] = True
            res['total'] = get_count(total)
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al obtener los libros, inténtelo nuevamente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

    @staticmethod
    def getBook(book_id, db, response):
        try:
            res = {
                'success': False,
            }
            book = database.Libro.query.get(book_id)
            res['success'] = True
            res['book'] = book
        except Exception as e:
            print(e)
            # db.session.rollback()
            res['msg'] = 'Hubo un error al cargar el libro, inténtelo nuevamente'
        finally:
            # return response(json.dumps(res), mimetype='application/json')
            return render_template('book.html', )

    @staticmethod
    def searchBook(query_p, db, response):
        try:
            res = {
                'success': False,
            }
            books = database.Libro.query.filter(
                    database.Libro.autor.like('%{}%'.format(query_p)) |
                    database.Libro.nombre_libro.like('%{}%'.format(query_p)),
                    database.Libro.activo == 1
                    ).all()
            if books == None:
                res['books'] = []
            else:
                # print(books.comentarios)
                serialized = [ { 'id': i.id,
                                'name': i.nombre_libro,
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
            res['msg'] = 'Hubo un error al cargar el libro, inténtelo nuevamente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

    @staticmethod
    def denounceBook(db, request, response):
        try:
            res = {
                'success': False,
            }
            book = database.Libro.query.get(request.form['id'])
            book.denuncia_derechos = request.form['desc']
            book.activo = False
            db.session.commit()
            res['success'] = True
            res['msg'] = 'El libro que subió acaba de ser denunciado, revisaremos su solicitud, por el momento ha sido dado de baja de la LIBREria, recargue la página para ver los cambios'
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
                    newBook = database.Libro(
                        nombre_libro=request.form['book'],
                        genero=request.form['genre'],
                        autor=request.form['author'],
                        idioma=request.form['language'],
                        licencia=request.form['licence'],
                        nombre_archivo=bookfilename,
                        imagen=imgfilename,
                    )
                    bookfile.save(os.path.join(env['UPLOADS_DIR'] + '/books', bookfilename))
                    if imgfilename != None: imgfile.save(os.path.join(env['UPLOADS_DIR'] + '/images', imgfilename))
                    db.session.add(newBook)
                    db.session.commit()
                    res['success'] = True
                    res['route'] = 'libro-exito'
                else:
                    print('err')
                    res['success'] = False
                    res['msg'] = 'Formato no aceptado'
                    res['code'] = 400
            else:
                res['success'] = True
                res['route'] = 'libro-exito'
        except Exception as e:
            print(e)
            db.session.rollback()
            res['route'] = 'libro-error'
        finally:
            return response(json.dumps(res), mimetype='application/json')
