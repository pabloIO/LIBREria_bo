from flask import Flask, render_template, Response, request, make_response, session, url_for, redirect, flash, g, jsonify
from flask_cors import CORS, cross_origin
from config.config import env
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required , get_jwt_identity, unset_jwt_cookies

###revisar xd
'''
app = Flask(__name__, template_folder="public")
mysql = MySQL()
app.config['MYSQL_HOST']= env['HOST']
app.config['MYSQL_USER']= env['SQL_CONF']['USER_NAME']
app.config['MYSQL_PASSWORD'] = env['SQL_CONF']['PASSWORD']
app.config['MYSQL_DB'] = env['SQL_CONF']['DB_NAME']
mysql.init_app(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = env['UPLOADS_DIR']
## DATABASE CONFIG AND INSTANTIATION
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
db = SQLAlchemy(app)
'''

app = Flask(__name__, template_folder="public", static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = env['APP_SECRET']
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/user'
app.config['JWT_SECRET_KEY'] = env['APP_SECRET'] 
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
# cors = CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}})

db = SQLAlchemy(app)
jwt = JWTManager(app)

from models import tables
from controllers import libros_ctrl, poem_ctrl, login_ctrl, users_ctrl
from middleware.json_middleware import json_required

@app.before_first_request
def create_tables():
    print('create tables')
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

#############################
####### VIEWS ROUTES ########
#############################
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/nosotros")
def about():
    return render_template('about.html')

@app.route("/poema")
def universe():
    return render_template('universe.html')

@app.route("/poemafinal")
def poemafinal():
    return render_template('poemafinal.html')

@app.route("/licencias")
def licencias():
    return render_template('licencias.html')

@app.route("/bibliotecas")
def bibliotecas():
    return render_template('bibliotecas.html')

'''
AUTHENTICATION
'''
@app.route(env['API_VERSION'] + "/login", methods=['POST'])
@json_required
# @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def authenticate():
    return login_ctrl.LoginCtrl.login()

@app.route(env['API_VERSION'] + "/sign_in", methods=['POST'])
@json_required
# @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def sign_in():
    return login_ctrl.LoginCtrl.register()

@app.route("/login", methods=['GET'])
# @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def login():
    return render_template('login.html')

@app.route('/registro', methods = ['GET'])
def register():
    return render_template('register.html')

@app.route(env['API_VERSION'] + '/user/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    print('logouuuuut!')
    unset_jwt_cookies(resp)
    return resp, 200
'''
USER
'''
@app.route('/user/dashboard', methods = ['GET'])
@jwt_required
def dashboard():
    return render_template('views-users/user_dashboard.html')

@app.route("/user/nosotros")
def user_about():
    return render_template('views-users/about.html')

@app.route("/user/poema")
def user_universe():
    return render_template('views-users/universe.html')

@app.route("/user/poemafinal")
def user_poemafinal():
    return render_template('views-users/poemafinal.html')

@app.route("/user/licencias")
def user_licencias():
    return render_template('views-users/licencias.html')

@app.route("/user/bibliotecas")
def user_bibliotecas():
    return render_template('views-users/bibliotecas.html')


############################################
##### PERFIL DE USUARIO##############
############################################
@app.route('/user/perfil', methods = ['GET'])
@jwt_required
def profile():
    return render_template('views-user-perfil/perfil.html')


@app.route("/user/autor/my-books", methods=['GET'])
def get_my_books():
    return render_template('views-user-perfil/mis-libros.html')

@app.route("/user/autor/my-books/<book_id>", methods=['GET'])
def get_my_book_stats(book_id):
    return render_template('views-user-perfil/estadisticas-libro.html')

@app.route('/user/favorito')
def mis_favoritos():
    return render_template('views-user-perfil/favoritos.html')

@app.route('/user/config')
def config():
    return render_template('views-user-perfil/configuracion.html')

@app.route('/user/seguidores')
def seguidores():
    return render_template('views-user-perfil/seguidores.html')

@app.route('/user/siguiendo')
def siguiendo():
    return render_template('views-user-perfil/siguiendo.html')
#################################################
############### FIN #############################
#################################################

@app.route('/cookie')
def cookie():
    resp = make_response( render_template('cookie.html') )
    resp.set_cookie('custome_cookie', 'Owo')
    return resp

## CREAR ESTAS DOS PAGINAS
@app.route("/user/libro-exito")
@jwt_required
def upload_success():
    return render_template('libro-exito.html')

@app.route("/user/libro-error")
def upload_fail():
    return render_template('libro-error.html')

##Redirección correcta al subir verso en universos.html
@app.route("/verso-exito")
def upload_poem_success():
    return render_template('universe.html')

@app.route("/user/libro/<book_id>", methods=['GET'])
def get_book(book_id):
    return render_template('views-users/ver-libro.html')

#############################
#############################
#############################

#############################
####### BOOKS ROUTES ########
#############################
@app.route(env['API_VERSION'] + "/libros/page/<page_num>", methods=['GET'])
# @jwt_required
def books(page_num):
    return libros_ctrl.LibrosCtrl.all(page_num)

@app.route(env['API_VERSION'] + "/libros/search/<criteria>", methods=['GET'])
def books_search(criteria):
    return libros_ctrl.LibrosCtrl.searchBook(criteria, db, Response)

@app.route(env['API_VERSION'] + "/libros/<book_id>", methods=['GET'])
def book(book_id):
    return libros_ctrl.LibrosCtrl.getBook(book_id)

@app.route(env['API_VERSION'] + "/libro/upload", methods=['POST', 'GET'])
# @jwt_required
def upload_book():
    return libros_ctrl.LibrosCtrl.uploadBook(db, request, Response)

@app.route(env['API_VERSION'] + "/libro/download/<book_id>", methods=['GET'])
# @jwt_required
def download_book(book_id):
    return libros_ctrl.LibrosCtrl.downloadBook(book_id)

@app.route(env['API_VERSION'] + "/libro/denounce", methods=['POST', 'GET'])
def denounce_book():
    return libros_ctrl.LibrosCtrl.denounceBook(db, request, Response)

@app.route(env['API_VERSION'] + "/profile/<user_id>", methods=['GET'])
def get_user_data(user_id):
    return users_ctrl.UserCtrl.getUser(user_id)

@app.route(env['API_VERSION'] + "/profile/books/<autor_id>", methods=['GET'])
def get_autor_books(autor_id):
    return users_ctrl.UserCtrl.getBooks(autor_id)

@app.route(env['API_VERSION'] + "/profile/books/info/<book_id>", methods=['GET'])
def get_book_stats(book_id):
    return libros_ctrl.LibrosCtrl.getBookStatistics(book_id)

#############################
#############################
#############################

#############################
####### POEM ROUTES ########
#############################

##Ruta que devuelve el objeto JSON con el contenido de la tabla <Poema>
@app.route(env['API_VERSION'] + "/poems/page", methods=['GET'])
def poema_lineas():
    return poem_ctrl.PoemCtrl.all(db, Response)

##Ruta que agrega una nueva tupla a la tabla <Poema>
@app.route(env['API_VERSION'] + "/poems/upload/<verso>", methods=['POST'])
def upload_poem(verso):
    return poem_ctrl.PoemCtrl.uploadPoem(db, request, verso, Response)

@app.route('/Enviar',methods=['POST','GET'])
def Enviar():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password:
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Registrado con exito'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Ingrese datos validos</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

#############################
#############################
#############################

# @app.route("/chat_room")
# def chat_room():
#     return render_template('chatRoom.html')
#


# @app.route('/user/<user_id>/conversation')
# def show_user_conversation(user_id):
#     return chat_ctrl.ChatCtrl.getConversation(user_id, db, Response)
#
# @app.route('/user/<user_id>/conversation/user-text')
# def show_conversation_text(user_id):
#     return chat_ctrl.ChatCtrl.getConversationText(user_id, db, Response)

if __name__ == '__main__':
    print(str.format('CONECTADO EN PUERTO {0}', env['PORT']))
    app.run(host=env['HOST'], port=env['PORT'], debug=True)
