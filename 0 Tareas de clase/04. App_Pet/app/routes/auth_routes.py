from flask import Blueprint, request, jsonify
import secrets
from ..models.user_model import create_user, verify_user

auth_bp = Blueprint("auth", __name__)

# Diccionario simple en memoria para tokens (solo para la tarea)
TOKENS = {}

# POST /auth/signup  -> SignIn user (rol por defecto client)
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user, err = create_user(email, password, role="client")
    if err:
        return jsonify({"error": err}), 400

    return jsonify({
        "message": "User created",
        "email": user["email"],
        "role": user["role"]
    }), 201

# POST /auth/create  -> Create user con rol configurable (ej: admin)
@auth_bp.route("/create", methods=["POST"])
def create():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "client")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user, err = create_user(email, password, role=role)
    if err:
        return jsonify({"error": err}), 400

    return jsonify({
        "message": "User created (admin endpoint)",
        "email": user["email"],
        "role": user["role"]
    }), 201

# POST /auth/login  -> Login user (devuelve token sencillo)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = verify_user(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = secrets.token_hex(16)
    TOKENS[token] = {
        "email": user["email"],
        "role": user["role"]
    }

    return jsonify({
        "message": "Login ok",
        "token": token
    }), 200
