from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
# from typing import TypedDict


import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


# class Person(TypedDict):
#     id: int
#     name: str
#     age: int
#     isMale: bool


# persons: list[Person] = [
#     {"id": 1, "name": "John", "age": 23, "isMale": True},
#     {"id": 2, "name": "Ann", "age": 19, "isMale": False},
# ]

app = Flask(__name__)
CORS(app)


# DATABASE CONNECTION
def db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )


@app.route("/")
def home():
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Person API is running",
            "database": "connected"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Person API is running",
            "database": "connection failed",
            "error": str(e)
        }), 500


# GET ALL PERSONS
@app.route("/persons", methods=["GET"])
def get_persons():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM persons")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows), 200


# GET ONE PERSON
@app.route("/persons/<int:id>", methods=["GET"])
def get_person(id):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM persons WHERE id = %s", (id,))
    person = cursor.fetchone()

    cursor.close()
    conn.close()

    if not person:
        return jsonify({"error": f"No person with id: {id}"}), 404

    return jsonify(person), 200


# CREATE PERSON
@app.route("/persons", methods=["POST"])
def create_person():
    body = request.get_json()

    name = body.get("name")
    age = body.get("age")
    is_male = body.get("isMale")

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO persons (name, age, isMale) VALUES (%s, %s, %s)",
        (name, age, is_male)
    )

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "age": age,
        "isMale": is_male
    }), 201


# UPDATE PERSON
@app.route("/persons/<int:id>", methods=["PUT"])
def update_person(id):
    body = request.get_json()

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE persons SET name=%s, age=%s, isMale=%s WHERE id=%s",
        (body.get("name"), body.get("age"), body.get("isMale"), id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": f"No person with id: {id}"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": f"Person {id} updated"}), 200


# DELETE PERSON
@app.route("/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM persons WHERE id=%s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": f"No person with id: {id}"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": f"Person {id} deleted"}), 200


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


if __name__ == "__main__":
    print("Flask App is running...")
    app.run(host="0.0.0.0", port=5000, debug=True)

