from flask import Flask
from flask_bcrypt import Bcrypt
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from resources.errors import errors
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

app = Flask(__name__)
# app.config['MONGODB_DB'] = os.environ['MONGODB_DATABASE']
# app.config['MONGODB_HOST'] = os.environ['MONGODB_HOSTNAME'] 
# app.config['MONGODB_USERNAME'] = os.environ['MONGODB_USERNAME'] 
# app.config['MONGODB_PASSWORD'] = os.environ['MONGODB_PASSWORD'] 
app.config['MONGODB_SETTINGS'] = {
    'db' : 'prook',
    'username' : 'prook',
    'password' : 'm0Zs7d89nMmGqpwfV7hK9BdvGY7',
    'host': "mongodb://127.0.0.1:27017/prook?authSource=admin"
}
app.config['MONGODB_PORT'] = 27017
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY'] 

api = Api(app,errors=errors)
bcrypt = Bcrypt(app)
cors = CORS(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
