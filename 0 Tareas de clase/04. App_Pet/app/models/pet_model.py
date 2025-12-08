from bson import ObjectId
from ..db import get_db

def seed_pets():
    db = get_db()
    if db.pets.count_documents({}) == 0:
        pets = [
            {
                "name": "Firu",
                "species": "dog",
                "age": 3,
                "owner": "Ana",
                "vaccinated": True
            },
            {
                "name": "Misu",
                "species": "cat",
                "age": 2,
                "owner": "Luis",
                "vaccinated": False
            },
            {
                "name": "Rocky",
                "species": "dog",
                "age": 5,
                "owner": "Carlos",
                "vaccinated": True
            },
            {
                "name": "Luna",
                "species": "rabbit",
                "age": 1,
                "owner": "Maria",
                "vaccinated": False
            },
            {
                "name": "Toby",
                "species": "dog",
                "age": 4,
                "owner": "Pedro",
                "vaccinated": True
            }
        ]
        db.pets.insert_many(pets)

def pet_to_json(pet_doc):
    pet_doc["id"] = str(pet_doc["_id"])
    del pet_doc["_id"]
    return pet_doc
