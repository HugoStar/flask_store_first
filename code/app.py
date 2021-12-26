from flask import Flask, request

from flask_jwt import JWT, jwt_required

from flask_restful import Api, Resource

from security import authenticate, identity


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)
api = Api(app)

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'An item wit name {name} already exists'}, 400
        data = request.get_json()
        item = {'name': name,
                'price': data['price'],
                }
        items.append(item)
        return item, 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)
