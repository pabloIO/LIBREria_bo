from flask import Flask, render_template, Response, request, make_response, session, url_for, redirect, flash, g, jsonify
from flask_cors import CORS, cross_origin
from config.config import env
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required , get_jwt_identity, unset_jwt_cookies
from flask_migrate import Migrate

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
app.config['SQLALCHEMY_DATABASE_URI'] = env['SQL_CONF']['DB_URI_MYSQL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = env['APP_SECRET']
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/user'
app.config['JWT_SECRET_KEY'] = env['APP_SECRET'] 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False 
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
# cors = CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}})

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

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
    return render_template('user_dashboard.html')

@app.route('/user/perfil', methods = ['GET'])
@jwt_required
def profile():
    return render_template('views/perfil.html')

@app.route('/user/perfil/<string:user_id>', methods = ['GET'])
@jwt_required
def user_profile(user_id):
    return render_template('views/user-perfil.html')


@app.route('/cookie')
def cookie():
    resp = make_response( render_template('cookie.html') )
    resp.set_cookie('custome_cookie', 'Owo')
    return resp

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

## CREAR ESTAS DOS PAGINAS
@app.route("/libro-exito/<book_id>")
# @jwt_required
def upload_success(book_id):
    return render_template('libro-exito.html')

@app.route("/libro-error")
def upload_fail():
    return render_template('libro-error.html')

##Redirección correcta al subir verso en universos.html
@app.route("/verso-exito")
def upload_poem_success():
    return render_template('universe.html')

@app.route("/user/libro/<book_id>", methods=['GET'])
def get_book(book_id):
    return render_template('ver-libro.html')

@app.route("/user/autor/my-books", methods=['GET'])
def get_my_books():
    return render_template('views/mis-libros.html')

@app.route("/user/autor/my-books/<book_id>", methods=['GET'])
def get_my_book_stats(book_id):
    return render_template('views/estadisticas-libro.html')

@app.route("/user/autor/my-books/stats", methods=['GET'])
def get_my_books_stats():
    return render_template('views/estadisticas-libros.html')

@app.route("/user/autor/followers", methods=['GET'])
def get_followers_view():
    return render_template('views/seguidores.html')

@app.route("/user/autor/following", methods=['GET'])
def get_following_view():
    return render_template('views/siguiendo.html')

@app.route("/user/autor/config")
def get_config():
    return render_template('views/configuracion.html')
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

@app.route(env['API_VERSION'] + "/libro/comment", methods=['POST'])
def comment_book():
    return libros_ctrl.LibrosCtrl.commentBook()

@app.route(env['API_VERSION'] + "/libro/upload", methods=['POST', 'GET'])
# @jwt_required
def upload_book():
    return libros_ctrl.LibrosCtrl.uploadBook(db, request, Response)

@app.route(env['API_VERSION'] + "/libro/download/<book_id>", methods=['GET'])
# @jwt_required
def download_book(book_id):
    return libros_ctrl.LibrosCtrl.downloadBook(book_id)

@app.route(env['API_VERSION'] + "/libro/<book_id>/denounce", methods=['PUT'])
def denounce_book(book_id):
    return libros_ctrl.LibrosCtrl.denounceBook(book_id)

@app.route(env['API_VERSION'] + "/libro/<book_id>/rate", methods=['PUT'])
def rate_book(book_id):
    return libros_ctrl.LibrosCtrl.rateBook(book_id)

@app.route(env['API_VERSION'] + "/libro/<book_id>/rate/<autor_id>", methods=['GET'])
def get_rating(book_id, autor_id):
    return libros_ctrl.LibrosCtrl.getRating(book_id, autor_id)

@app.route(env['API_VERSION'] + "/profile-author/<author_id>", methods=['GET'])
def get_author_data(author_id):
    return users_ctrl.UserCtrl.getAuthor(author_id)

@app.route(env['API_VERSION'] + "/following/<user_id>/<follower_id>", methods=['GET'])
def user_following(user_id, follower_id):
    return users_ctrl.UserCtrl.followingUser(user_id, follower_id)

@app.route(env['API_VERSION'] + "/follow", methods=['POST'])
def follow_user():
    return users_ctrl.UserCtrl.followUser()

@app.route(env['API_VERSION'] + "/followers/<author_id>", methods=['GET'])
def get_followers(author_id):
    return users_ctrl.UserCtrl.getFollowers(author_id)

@app.route(env['API_VERSION'] + "/following/<author_id>", methods=['GET'])
def get_following(author_id):
    return users_ctrl.UserCtrl.getFollowing(author_id)

@app.route(env['API_VERSION'] + "/profile/books/<autor_id>", methods=['GET'])
def get_autor_books(autor_id):
    return users_ctrl.UserCtrl.getBooks(autor_id)

@app.route(env['API_VERSION'] + "/profile/books/info/<book_id>", methods=['GET'])
def get_book_stats(book_id):
    return libros_ctrl.LibrosCtrl.getBookStatistics(book_id)

@app.route(env['API_VERSION'] + "/profile/books/stats/<autor_id>", methods=['GET'])
def get_books_stats(autor_id):
    return libros_ctrl.LibrosCtrl.getBooksStatistics(autor_id)

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
