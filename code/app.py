from flask import Flask, request

from flask_jwt import JWT

from flask_restful import Api, Resource, reqparse

from security import authenticate, identity


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)
api = Api(app)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field connot be left blank!'
    )

    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
    
        data = Item.parser.parse_args()
    
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'An item wit name {name} already exists'}, 400
        
        item = {'name': name,
                'price': data['price'],
                }
                
        items.append(item)
        
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}, 201
        
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)
