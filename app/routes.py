from flask import Blueprint, request, jsonify
from .models import *
from .utils import hash_password, check_password

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def health():
    return jsonify({"status": "running"})

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(users), 200

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/users', methods=['POST'])
def create():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not all([name, email, password]):
        return jsonify({"error": "Missing fields"}), 400
    try:
        user_id = create_user(name, email, hash_password(password))
        return jsonify({"message": "User created", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not all([name, email]):
        return jsonify({"error": "Missing fields"}), 400
    update_user(user_id, name, email)
    return jsonify({"message": "User updated"}), 200

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    delete_user(user_id)
    return jsonify({"message": f"User {user_id} deleted"}), 200

@user_bp.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Name parameter required"}), 400
    results = search_users_by_name(name)
    return jsonify(results), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not all([email, password]):
        return jsonify({"error": "Missing fields"}), 400
    user = verify_login(email, password)
    if user and check_password(user[1], password):
        return jsonify({"status": "success", "user_id": user[0]}), 200
    return jsonify({"status": "failed"}), 401