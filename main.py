from flask import Flask, request, jsonify, render_template
import socket
import json
import os
import requests

YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'

TRIVIA_FILE = 'trivia_data.json'
HTML_FILE = 'index.html'
CSS_FILE = None

with open(TRIVIA_FILE, 'r') as file:
    trivia_data = json.load(file)

app = Flask(__name__, template_folder='templates')

@app.route('/')
def welcome():
    return render_template(HTML_FILE)


@app.route('/trivia', methods=['GET'])
def get_all_trivia_questions():
    return jsonify(trivia_data)


@app.route('/trivia/delete/<int:index>', methods=['DELETE'])
def delete_trivia_question(index):
    global trivia_data

    if 0 <= index < len(trivia_data['results']):
        del trivia_data['results'][index]
        with open('trivia_data.json', 'w') as file:
            json.dump(trivia_data, file, indent=4)
        return jsonify({'message': 'Trivia question deleted successfully'})
    else:
        return jsonify({'error': 'Invalid index'})


@app.route('/trivia/add', methods=['POST'])
def add_trivia_question():
    global trivia_data
    new_question = request.json
    trivia_data.append(new_question)
    with open('trivia_data.json', 'w') as file:
        json.dump(trivia_data, file, indent=4)

    return jsonify({'message': 'Trivia question added successfully'})


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

