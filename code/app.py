from datetime import timedelta

from flask import Flask

from flask_jwt import JWT

from flask_restful import Api

from resources.item import Item, ItemList
from resources.user import UserRegister

from security import authenticate, identity


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)
api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000)
