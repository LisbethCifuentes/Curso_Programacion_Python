from werkzeug.security import generate_password_hash, check_password_hash
from ..db import get_db

def create_user(email, password, role="client"):
    db = get_db()
    if db.users.find_one({"email": email}):
        return None, "User already exists"

    hashed = generate_password_hash(password)
    user_doc = {
        "email": email,
        "password": hashed,
        "role": role
    }
    result = db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc, None

def verify_user(email, password):
    db = get_db()
    user = db.users.find_one({"email": email})
    if not user:
        return None
    if not check_password_hash(user["password"], password):
        return None
    return user
