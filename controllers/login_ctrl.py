import sys
import os.path
import json
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from models import sesion
import models.models as database
from sqlalchemy.exc import IntegrityError
import uuid
from config.config import env

class LoginCtrl(object):
    @staticmethod
    def login(db, request, response):
        try:
            res = {
                'success': False,
            }
            exists = database.Usuarios.query.filter_by(
                nombre_usuario=request['username']
            ).first()
            if exists:
                newSession = database.Sesion(
                    usuarios_id=exists.id
                )
                db.session.add(newSession)
                db.session.commit()
                res['success'] = True
                res['id'] = exists.id
                res['username'] = exists.nombre_usuario
                res['token'] = uuid.uuid4().hex,
                res['sesion'] = newSession.id,
                res['socket_channel'] = exists.canal_socket,
                res['_conversation_id'] = exists._conversation_id
                res['url_to'] = str.format('{0}:{1}/chat_room',  'http://localhost', env['PORT'])
            else:
                if not request['username']:
                    res['msg'] = 'Debes introducir el nombre de usuario'
                    return response(json.dumps(res), mimetype='application/json')
                newUser = database.Usuarios(
                    nombre_usuario=request['username'],
                    canal_socket=uuid.uuid4().hex,
                    _conversation_id=str(mongo.create_conversation())
                )
                db.session.add(newUser)
                db.session.commit()
                newSession = database.Sesion(
                    usuarios_id=newUser.id
                )
                db.session.add(newSession)
                db.session.commit()
                res['success'] = True
                res['id'] = newUser.id
                res['sesion'] = newSession.id,
                res['username'] = newUser.nombre_usuario
                res['token'] = uuid.uuid4().hex
                res['socket_channel'] = newUser.canal_socket,
                res['_conversation_id'] = newUser._conversation_id
                res['url_to'] = str.format('{0}:{1}/chat_room', 'http://localhost', env['PORT'])
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            res['msg'] = 'Nombre de usuario existente'
        finally:
            return response(json.dumps(res), mimetype='application/json')
