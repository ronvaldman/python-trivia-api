from flask import Flask, request, jsonify, render_template
import socket
import json
import os
import random

YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'

TRIVIA_FILE = 'trivia_data.json'
HTML_FILE = 'index.html'
CSS_FILE = None
JSON_DATA_FILE = 'trivia_data.json'

with open(TRIVIA_FILE, 'r') as file:
    trivia_data = json.load(file)

app = Flask(__name__, template_folder='templates')


def load_json_data():
    with open(JSON_DATA_FILE, 'r') as file:
        return json.load(file)


def save_json_data(data):
    with open(JSON_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/')
def welcome():
    return render_template(HTML_FILE)


@app.route('/trivia', methods=['GET'])
def get_all_trivia_questions():
    return jsonify(trivia_data)


@app.route('/trivia/<int:question_id>', methods=['GET'])
def get_specific_question(question_id):
    if 0 <= question_id < len(trivia_data):
        return jsonify(trivia_data[question_id])
    else:
        return jsonify({'error': 'Invalid question ID'})


@app.route('/trivia/delete/<int:question_id>', methods=['DELETE'])
def delete_trivia_question(question_id):
    trivia_data = load_json_data()
    for question in trivia_data:
        if question['id'] == question_id:
            trivia_data.remove(question)
            save_json_data(trivia_data)
            return jsonify({'message': f'Trivia question with ID {question_id} deleted successfully'})
    return jsonify({'error': f'Question with ID {question_id} not found'})


def is_question_duplicate(new_question):
    trivia_data = load_json_data()
    for question in trivia_data:
        if question['question'] == new_question['question']:
            return True
    return False


@app.route('/trivia/add', methods=['POST'])
def add_trivia_question():
    global trivia_data
    if request.method == 'POST':
        new_question = request.json
        if new_question not in trivia_data and all(new_question['id'] != question['id'] for question in trivia_data) and not is_question_duplicate(new_question):
            trivia_data.append(new_question)
            save_json_data(trivia_data)
            return jsonify({'message': 'Trivia question added successfully'})
        else:
            return jsonify({'error': 'Duplicate question'})
    else:
        return jsonify({'error': 'Only POST requests are allowed for this endpoint'})


@app.route('/trivia/random', methods=['GET'])
def get_random_question():
    trivia_data = load_json_data()
    random_question = random.choice(trivia_data)
    return jsonify(random_question)


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


if __name__ == '__main__':
    username = os.getlogin()
    print(GREEN + "Hello,", username + "!", "Welcome to Ron's trivia API!")
    while True:
        port_input = input(RED + "Select a port for your Flask server: ")
        if port_input.strip() and port_input.isdigit():
            port = int(port_input)
            if not is_port_in_use(port):
                print(GREEN + " * Server address is localhost:{}".format(port))
                app.run(port=port, debug=True)
                break
            else:
                print(RED + "Port {} is already in use. Please select a different port.".format(port))
        else:
            port = 5000
            if not is_port_in_use(port):
                print(GREEN + "Default server address is localhost:{}".format(port))
                app.run(port=port)
                break
