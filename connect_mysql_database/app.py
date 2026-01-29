from flask import Flask, jsonify
import mysql.connector
import os
from dotenv import load_dotenv


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")



# Create the flask app
app = Flask(__name__)

# DATABASE CONNECTION
def db_connection():
    return mysql.connector.Connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# Home Page
@app.route('/')
def index():
    return "Welcome Page"

# READ FROM DATABASE
@app.route('/users')
def get_all_users():
    conn = db_connection() # connect to databse 
    cursor = conn.cursor() # create cursor


    sql = "SELECT * FROM users"
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(results)


# WRITE TO DATABASE
@app.route('/add-user')
def add_user():
    conn = db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = ("John Doe", "john@example.com")

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return "Added User"


# Run app
if __name__ == "__main__":
    print("Starting App Run")
    print("Connected to: ",DB_HOST, DB_USER, DB_NAME)
    app.run(debug=True, port=5000)


