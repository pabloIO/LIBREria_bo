import sys
import os.path
import json
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from models import sesion
# import models.models as database
from sqlalchemy.exc import IntegrityError
import uuid
from app import db
from flask import Response, request, jsonify, render_template, make_response
from config.config import env
from models import tables
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies
)

class LoginCtrl(object):
    @staticmethod
    def login():
        try:
            res = {
                'success': False,
            }
            req = request.get_json()
            user = tables.Usuario.exists(req['username']) 
            if user:
                if not tables.Usuario.check_password(req['password'], user.us_password):
                    res['msg'] = 'Credenciales incorrectos'
                    res['code'] = 200
                else:
                    # print(user.autor[0].ai_id)
                    access_token = create_access_token(identity=req['username'])
                    res['msg'] = 'Exito'
                    res['success'] = True
                    res['code'] = 200
                    res['user'] = {
                        'id': user.us_id,
                        'email': user.us_correo,
                        'name': user.complete_name(),
                        'image': user.us_foto_perfil,
                        'socket': user.us_canal_socket,
                        'rol': user.rol_id,
                        'token': access_token,
                        'autor_id': user.autor[0].ai_id,
                    }
                    resp = jsonify(res)
                    set_access_cookies(resp, access_token)
                    
            else:
                res['code'] = 200
                res['msg'] = 'El usuario no existe, verifique sus datos'
                resp = jsonify(res)
            return resp, 200
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error en la petición, intente nuevamente'
            res['code'] = 500
            return jsonify(res)
    @staticmethod
    def register():
        try:
            res = {'success': False}
            req = request.get_json()
            if not tables.Usuario.exists(req['email']) :
                user = tables.Usuario(
                    us_nombre_usuario=req['username'],
                    us_nombre=req['name'],
                    us_apellidos=req['lastname'],
                    us_correo=req['email'],
                    us_password=tables.Usuario.hash_password(req['password']),
                    rol_id=1,
                )
                autor = tables.AutorIndie()
                user.autor.append(autor)
                # print(user)
                # return
                tables.Usuario.save(user)
                # print(created)

                res['success'] = True
                res['msg'] = 'Se creo un usuario con exito'
                access_token = create_access_token(identity=req['username'])
                res['code'] = 200
                res['user'] = {
                    'id': user.us_id,
                    'email': user.us_correo,
                    'name': user.complete_name(),
                    'image': user.us_foto_perfil,
                    'socket': user.us_canal_socket,
                    'rol': user.rol_id,
                    'token': access_token,
                }
                set_access_cookies(jsonify(res), access_token)

            else:
                res['msg'] = 'Usuario existente'
            return jsonify(res)
        except Exception as e:
            print(e)
            res['msg'] = 'Hubo un error al registrarse, inténtelo de nuevo'
            res['code'] = 500
            return jsonify(res)