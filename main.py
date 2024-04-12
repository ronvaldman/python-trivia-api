from flask import Flask, request, jsonify, render_template
import socket
import json
import os
import requests
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


@app.route('/trivia/delete/<int:index>', methods=['DELETE'])
def delete_trivia_question(index):
    trivia_data = load_json_data()

    if 0 <= index < len(trivia_data):
        del trivia_data[index]
        save_json_data(trivia_data)
        return jsonify({'message': 'Trivia question deleted successfully'})
    else:
        return jsonify({'error': 'Invalid index'})


@app.route('/trivia/add', methods=['POST'])
def add_trivia_question():
    global trivia_data
    if request.method == 'POST':
        new_question = request.json
        if isinstance(trivia_data, dict):
            trivia_data = [trivia_data]
        trivia_data.append(new_question)
        with open('trivia_data.json', 'w') as file:
            json.dump(trivia_data, file, indent=4)
        return jsonify({'message': 'Trivia question added successfully'})
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
    port = 5000
    while True:
        port = int(input(RED+"Select a port for your Flask server: "))
        if not is_port_in_use(port):
            print(GREEN + "Server address is 127.0.0.1:{}".format(port))
            app.run(port=port)
            break
        # elif (port==""):
        #     port = 5000
        else:
            print(RED + "Port {} is already in use. Please select a different port.".format(port))
