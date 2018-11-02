import string, random, json, sys, os.path, uuid
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from models import sesion
import models.models as database
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import func
import uuid
from config.config import env
from werkzeug.utils import secure_filename
from flask import flash, redirect, url_for, jsonify

def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

class PoemCtrl(object):
    @staticmethod
    def all(db, response):
        try:
            res = {
                'success': False,
            }
            total = database.Poema.query.filter(database.Poema.activo == 1)
            if total == None:
                res['books'] = []
            else:
                serialized = [ { 'id': i.id,
                                'verso': i.verso
                               } for i in total ]
                res['books'] = serialized
            res['success'] = True
            res['total'] = get_count(total)
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al obtener los libros, inténtelo nuevamente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

    @staticmethod
    def getPoem(db, response):
        try:
            res = {
                'success': False,
            }
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error cargar uniVERSOS, inténtelo nuevamente'
        finally:
            return response(json.dumps(res), mimetype='application/json')

    @staticmethod
    def uploadPoem(db, request, verso, response):
        print(request)
        try:
            res = {
                'success': True,
            }
            if request.method == 'POST':
                newBook = database.Poema(
                    verso = verso[0:140],
                )
                db.session.add(newBook)
                db.session.commit()
                flash('Verso agregado con exito a poema')
                return response(json.dumps(res), mimetype='application/json')
                # return redirect(url_for('upload_poem_success'))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Hubo un error al agregar un nuevo elemento a uniVERSOS')
            return response(json.dumps(res), mimetype='application/json')
