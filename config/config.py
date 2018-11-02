from flask import Flask
import os


env = {
    'PORT'      : 5000,
    'HOST'      : '0.0.0.0',
    'APP_ENV'   : 'DEV',
    ##'APP_SECRET': 'libr0s_abiert0s',
    'APP_SECRET': 'libre2018User_',
    'APP'       : Flask(__name__, template_folder="public"),
    'SQL_CONF'  : {
        'DB_NAME'  : 'libreria',
        'USER_NAME': 'Libre',
        'PASSWORD': 'libre2018User_',
        
        'DB_URI'   :  'mysql+pymysql://root:@localhost/libreria',
        #'DB_URI'   : str.format('sqlite:///{0}', os.path.abspath('database/libreria.db')) if 'PYTHONANYWHERE_DOMAIN' not in  os.environ else 'sqlite:////home/lalibreria/LIBREria/database/libreria.db',
    },
    'UPLOADS_DIR': os.path.abspath('static') if 'PYTHONANYWHERE_DOMAIN' not in  os.environ else os.path.abspath('LIBREria/static'),
    'ALLOWED_EXTENSIONS_BOOKS': set(['pdf', 'txt', 'doc', 'docx', 'odt', 'epub']),
    'ALLOWED_EXTENSIONS_IMG': set(['png', 'svg', 'gif', 'jpg', 'jpeg']),
    'API_VERSION': '/api/v1',
    'MAX_FILE_SIZE': '200Mb',
}
