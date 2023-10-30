from flask import Blueprint, jsonify, request
from backend.models.todo import Todo
from backend.extensions import db

todo_routes = Blueprint('todo_routes', __name__)


@todo_routes.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    new_todo = Todo(title=data['title'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo added!'}), 201


@todo_routes.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todo_list = [{'id': todo.id, 'title': todo.title, 'done': todo.done} for todo in todos]
    return jsonify({'todos': todo_list})


@todo_routes.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'id': todo.id, 'title': todo.title})


@todo_routes.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    todo.title = data['title']
    db.session.commit()
    return jsonify({'message': 'Todo updated!'})


@todo_routes.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted!'})


@todo_routes.route('/todos/<int:todo_id>/toggle', methods=['PUT'])
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully', 'todo': {'id': todo.id, 'title': todo.title, 'done': todo.done}})