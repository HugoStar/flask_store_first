from datetime import timedelta
import os

from db import db

from flask import Flask

from flask_jwt import JWT

from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

from security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MY_DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


jwt = JWT(app, authenticate, identity)
api = Api(app)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)
