import json
from flask import Flask, request, jsonify

TODO_FILE = 'todos.json'

app = Flask(__name__)

def load_todos():
    try:
        with open(TODO_FILE, 'r') as file:
            todos = json.load(file)
            
    except FileNotFoundError:
        todos = []
    return todos

def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=4)

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = load_todos()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    todos = load_todos()

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')

    todo = {
        'id': len(todos) + 1,
        'title': title,
        'description': description,
        'status': status
    }

    todos.append(todo)
    save_todos(todos)
    return jsonify(todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todos = load_todos()

    for todo in todos:
        if todo['id'] == todo_id:
            data = request.get_json()
            title = data.get('title')
            description = data.get('description')
            status = data.get('status')

            todo['title'] = title
            todo['description'] = description
            todo['status'] = status

            save_todos(todos)
            return jsonify(todo)

    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = load_todos()

    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            save_todos(todos)
            return jsonify({'message': 'Todo deleted'})

    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
