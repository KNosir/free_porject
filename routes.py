from flask import jsonify, request, Blueprint
from data_model import UserAccounts
from actions_data import *

app = Blueprint('routes', __name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "server is up and running..."}), 200


@app.route('/accounts', methods=['GET'])
def accounts():
    return get_all_accounts()


@app.route('/accounts/<int:id>/details', methods=['GET'])
def account_by_id(id):
    try:
        return jsonify(get_all_accounts('', '', id))
    except:
        return {'status': 'user not found'}, 404


@app.route('/accounts', methods=['POST'])
def create():
    data = request.get_json()
    try:
        acc = UserAccounts(
            user_name=data['user_name'], account_number=data['account_number'])
        create_account(acc)
        return {'status': 'succesfully added'}, 201
    except:
        return {'status': 'account number found in data'}, 404


@app.route('/accounts/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    try:
        update_user_name(id, data['user_name'])
        return {"status": 'Success'}, 201
    except:
        return {'status': 'not found user'}, 404


@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        delete_account(id)
        return {'status': 'Success'}, 201
    except:
        return {'status': 'user not found'}, 404
