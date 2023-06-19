from flask import Blueprint, jsonify, request
from chat import load_chat
import json
import logging

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@main_bp.route('/api/chat/<is_new_chat>', methods=['POST'])
def index(is_new_chat):
    is_new_chat = is_new_chat == 'true'
    data = request.json
    response = {
        "data" : None,
        "error" : None
    }
    statusCode = 404
    try:
        address = request.headers['address']
        conversation = load_chat(address, is_new_chat)
        message = data['message']
        output = conversation.predict(input=message)
        logging.info(output)
        response['data'] = json.loads(output)
        statusCode = 200
    except Exception as error:
        logging.error(error)
        response['error'] = {
        'message': f"{error}"
        }
        statusCode = 404
    return jsonify(response), statusCode