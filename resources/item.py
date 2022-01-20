# from flask_jwt import jwt_required

from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field connot be left blank!')

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='This field connot be left blank!')

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message': f'An item wit name {name} already exists'}, 400

        item = ItemModel(name, **data)

        try:
            item.save_to_db()

        except Exception as e:
            print(e)
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_to_db()

        return {'message': 'item delete'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
