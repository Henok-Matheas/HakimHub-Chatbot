from flask import Blueprint, jsonify, request
from chat import load_chat
import json

main_bp = Blueprint('main', __name__)
conversation = load_chat()

@main_bp.route('/api/chat', methods=['POST'])
def index():
    data = request.json
    response = {''}
    statusCode = 404
    try:
        message = data['message']
        print(message)
        output = json.loads(conversation.predict(input=message))
        print(output, "this is output")
        response = {
        'data': output}
        statusCode = 200
    except Exception as e:
        response = {
        'message': f"An error occurred: {e}"}
        statusCode = 400
    return jsonify(response), statusCode