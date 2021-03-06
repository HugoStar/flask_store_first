from flask_jwt import jwt_required

from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'An store wit name {name} already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception:
            return {'message': 'An error occurred inserting the item'}, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_form_db()

        return {'message': 'Store delted'}


class StoreList(Resource):

    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
