from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Task
from .schemas import TaskSchema
from .extensions import db

task_bp = Blueprint('tasks', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Retrieve all tasks for the authenticated user
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: List of tasks
        schema:
          type: array
          items:
            $ref: '#/definitions/Task'
    """
    user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify(tasks_schema.dump(tasks))


@task_bp.route('/tasks/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    """
    Retrieve a specific task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task details
        schema:
          $ref: '#/definitions/Task'
      404:
        description: Task not found
    """
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(task_schema.dump(task))


@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Finish project"
            description:
              type: string
              example: "Complete the Flask task manager API"
    responses:
      201:
        description: Task created successfully
        schema:
          $ref: '#/definitions/Task'
    """
    data = request.get_json()
    user_id = int(get_jwt_identity())

    if not data or 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400

    task = Task(title=data['title'], description=data.get('description'), user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201


@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    """
    Update a specific task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the task
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Updated task"
            description:
              type: string
              example: "Updated description"
            completed:
              type: boolean
              example: true
    responses:
      200:
        description: Task updated successfully
        schema:
          $ref: '#/definitions/Task'
      404:
        description: Task not found
    """
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task_schema.dump(task))


@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """
    Delete a specific task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task deleted successfully
      404:
        description: Task not found
    """
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200
