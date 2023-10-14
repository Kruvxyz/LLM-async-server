from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from app.shared import shared
import threading
from app.background_process import be_run

app = Flask(__name__)
cors = CORS(app)


be = threading.Thread(target=be_run)
be.start()


@app.route('/ping', methods=['POST', 'GET'])
@cross_origin()
def state():
    return 'pong'


@app.route('/query', methods=['POST'])
@cross_origin()
def query():
    data = request.get_json()
    question = data.get("query")
    system = data.get("system", None)
    id = shared.add_question(question)
    return jsonify({"status": "ok", "id": id})


@app.route('/read', methods=['POST'])
@cross_origin()
def read():
    data = request.get_json()
    id = data.get("id")
    response = shared.get_response(id)
    return jsonify(response)
