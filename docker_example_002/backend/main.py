from flask import Flask, request, jsonify
from flask_cors import CORS


from typing import TypedDict

class Person(TypedDict):
    id: int
    name: str
    age: int
    isMale: bool


persons: list[Person] = [
    {"id": 1, "name": "John", "age": 23, "isMale": True},
    {"id": 2, "name": "Ann", "age": 19, "isMale": False},
]

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Person API is running"
    }), 200


@app.route("/persons", methods=["GET"])
def get_persons():
    return jsonify(persons), 200


@app.route("/persons/<int:id>", methods=["GET"])
def get_person(id):
    person = next((p for p in persons if p["id"] == id), None)

    if not person:
        return jsonify({
            "error": f"No person with id: {id}"
        }), 404

    return jsonify(person), 200


@app.route("/persons", methods=["POST"])
def create_person():
    # Accept JSON or form data
    body = request.get_json(silent=True)

    if not body:
        body = request.form.to_dict()

    # Validate required fields
    required_fields = ["name", "age", "isMale"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    # Validate and convert age
    try:
        age = int(body["age"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Age must be an integer"
        }), 400

    # Convert isMale to boolean
    is_male = body["isMale"]

    if isinstance(is_male, str):
        if is_male.lower() in ("true", "1", "yes"):
            is_male = True
        elif is_male.lower() in ("false", "0", "no"):
            is_male = False
        else:
            return jsonify({
                "error": "isMale must be true or false"
            }), 400

    elif not isinstance(is_male, bool):
        return jsonify({
            "error": "isMale must be a boolean"
        }), 400

    # Create new person
    new_person: Person = {
        "id": max(p["id"] for p in persons) + 1 if persons else 1,
        "name": str(body["name"]),
        "age": age,
        "isMale": is_male
    }

    persons.append(new_person)

    return jsonify(new_person), 201


@app.route("/persons/<int:id>", methods=["PUT"])
def update_person(id):
    person = next((p for p in persons if p["id"] == id), None)

    if not person:
        return jsonify({
            "error": f"No person with id: {id}"
        }), 404

    body = request.get_json(silent=True)

    if not body:
        return jsonify({
            "error": "No data provided"
        }), 400

    # Update name
    if "name" in body:
        person["name"] = str(body["name"])

    # Update age
    if "age" in body:
        try:
            person["age"] = int(body["age"])
        except (ValueError, TypeError):
            return jsonify({
                "error": "Age must be an integer"
            }), 400

    # Update isMale
    if "isMale" in body:
        is_male = body["isMale"]

        if isinstance(is_male, str):
            if is_male.lower() in ("true", "1", "yes"):
                is_male = True
            elif is_male.lower() in ("false", "0", "no"):
                is_male = False
            else:
                return jsonify({
                    "error": "isMale must be true or false"
                }), 400

        elif not isinstance(is_male, bool):
            return jsonify({
                "error": "isMale must be a boolean"
            }), 400

        person["isMale"] = is_male

    return jsonify(person), 200


@app.route("/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    person = next((p for p in persons if p["id"] == id), None)

    if not person:
        return jsonify({
            "error": f"No person with id: {id}"
        }), 404

    persons.remove(person)

    return jsonify({
        "message": f"Person {id} deleted successfully"
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Route not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed"
    }), 405


# if __name__ == "__main__":
#     print("Flask App is running...")
#     app.run(host="0.0.0.0", port=5000, debug=True)

