from flask import Blueprint, request, jsonify, render_template
from bson import ObjectId
from ..db import get_db
from ..models.pet_model import seed_pets, pet_to_json
from .auth_routes import TOKENS

pets_bp = Blueprint("pets", __name__, template_folder="../templates")

# -------- Helpers --------

def str_to_bool(value):
    if value is None:
        return None
    value = value.lower()
    if value in ["true", "1", "yes", "si", "sí"]:
        return True
    if value in ["false", "0", "no"]:
        return False
    return None

def require_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return TOKENS.get(token)

# Semilla de datos en Mongo (burned items -> Mongo)
@pets_bp.before_app_request
def ensure_seed():
    try:
        seed_pets()
    except Exception:
        # para evitar romper si hay errores de conexión en alguna petición
        pass

# -------- Endpoints JSON --------

# GET /pets/  -> lista con filtros (species, vaccinated)
@pets_bp.route("/", methods=["GET"])
def get_all_pets():
    db = get_db()
    species = request.args.get("species")
    vaccinated_param = request.args.get("vaccinated")
    vaccinated_bool = str_to_bool(vaccinated_param)

    query = {}
    if species:
        query["species"] = species
    if vaccinated_bool is not None:
        query["vaccinated"] = vaccinated_bool

    pets_cursor = db.pets.find(query)
    pets_list = [pet_to_json(p) for p in pets_cursor]
    return jsonify(pets_list), 200

# GET /pets/<id>  -> una sola mascota
@pets_bp.route("/<string:pet_id>", methods=["GET"])
def get_one_pet(pet_id):
    db = get_db()
    try:
        oid = ObjectId(pet_id)
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

    pet = db.pets.find_one({"_id": oid})
    if not pet:
        return jsonify({"error": "Pet not found"}), 404

    return jsonify(pet_to_json(pet)), 200

# POST /pets/  -> crear mascota (requiere token)
@pets_bp.route("/", methods=["POST"])
def create_pet():
    user = require_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    data = request.get_json() or {}

    if "name" not in data or "species" not in data:
        return jsonify({"error": "Fields 'name' and 'species' are required"}), 400

    new_pet = {
        "name": data["name"],
        "species": data["species"],
        "age": data.get("age"),
        "owner": data.get("owner"),
        "vaccinated": data.get("vaccinated", False),
        "created_by": user["email"]
    }

    result = db.pets.insert_one(new_pet)
    new_pet["_id"] = result.inserted_id
    return jsonify(pet_to_json(new_pet)), 201

# DELETE /pets/<id>  -> borrar mascota
@pets_bp.route("/<string:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    user = require_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    try:
        oid = ObjectId(pet_id)
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400

    result = db.pets.find_one_and_delete({"_id": oid})
    if not result:
        return jsonify({"error": "Pet not found"}), 404

    return jsonify({
        "message": "Pet deleted successfully",
        "deleted_pet": pet_to_json(result)
    }), 200

# -------- Endpoint SSR (Server Side Rendering) --------
# GET /pets/html -> devuelve página HTML con lista de mascotas
@pets_bp.route("/html", methods=["GET"])
def pets_html():
    db = get_db()
    pets_cursor = db.pets.find({})
    pets_list = list(pets_cursor)
    # Para que Jinja pueda usar el id si quieres
    for p in pets_list:
        p["id"] = str(p["_id"])
    return render_template("pets_list.html", pets=pets_list)
