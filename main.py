from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99,
            },
        ],
    },
]


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': [],
        }
    stores.append(new_store)
    return jsonify(new_store)


app.run(port=5000)
