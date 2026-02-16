from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)

# ---------------- HELPER FUNCTIONS ----------------
def format_products(items):
    """Format a list of products into a chatbot-friendly string."""
    if not items:
        return "No products found 😔"
    reply = "Available products:\n"
    for item in items:
        reply += f"- {item['name']} | ₦{item['price']:.2f} | Stock: {item['stock']}\n"
    return reply

def get_products_by_category(category_name):
    """Return all products in a given category."""
    query = """
        SELECT products.name, products.price, products.stock
        FROM products
        JOIN categories ON products.category_id = categories.id
        WHERE categories.name = %s
    """
    cursor.execute(query, (category_name,))
    return cursor.fetchall()

def get_products_by_price(max_price):
    """Return products under a given price."""
    query = "SELECT name, price, stock FROM products WHERE price <= %s"
    cursor.execute(query, (max_price,))
    return cursor.fetchall()

def log_chat(user_msg, bot_msg):
    """Store chat conversation into database."""
    cursor.execute(
        "INSERT INTO chat_logs (user_message, bot_reply) VALUES (%s, %s)",
        (user_msg, bot_msg)
    )
    db.commit()

# ---------------- CHATBOT LOGIC ----------------
def chatbot_response(user_message):
    user_message = user_message.lower().strip()
    user_words = user_message.split()
    
    # ---------- GREETINGS ----------
    if user_message in ["hi", "hello", "hey"]:
        return random.choice([
            "Hello! Welcome to our Nigerian fashion store 👗",
            "Hi there! How can I help you shop today? 😊",
            "Hey! Looking for something trendy today? 😎"
        ])
    
    # ---------- SMALL TALK ----------
    if "how are you" in user_message or "how's it going" in user_message:
        return random.choice([
            "I'm doing well, thank you! How about you? 😄",
            "All good here! Ready to help you find fashion items 👚",
            "I'm fine! Excited to help you shop for clothes today! 🛍️"
        ])
    
    if "who are you" in user_message or "your name" in user_message:
        return random.choice([
            "I'm your AI fashion sales assistant 🤖",
            "I help you find clothes, shoes, and accessories! 👗",
            "You can call me FashionBot! 😎"
        ])
    
    if user_message in ["thanks", "thank you"]:
        return random.choice([
            "You're welcome! 😄",
            "No problem! Happy shopping! 🛍️",
            "Glad I could help! 😊"
        ])
    
    if "happy" in user_message or "sad" in user_message:
        return random.choice([
            "I hope shopping brightens your day! 😊",
            "Cheer up! Maybe a new outfit will help 😎",
            "Fashion always lifts the mood! 👗"
        ])
    
    if "what can you do" in user_message or "help" in user_message:
        return ("I can help you check product categories, see prices, and find clothing for men, women, and more. "
                "You can also ask me about fashion, Nigeria, trends, or even for a joke! 😄")
    
    if "joke" in user_message:
        return random.choice([
            "Why did the belt go to jail? Because it held up a pair of pants! 😆",
            "I would tell you a joke about shoes, but it might be too soleful! 👟😂",
            "Why did the cloth go to school? To get a little material knowledge! 🤣"
        ])
    
    if "fashion" in user_message:
        return random.choice([
            "Nigeria has amazing fashion! From Ankara to Kaftan, we have it all 👗👔",
            "Fashion is life! Let's find something stylish for you 😎",
            "Love Nigerian fashion? You're in the right place! 🛍️"
        ])
    
    if "nigeria" in user_message:
        return random.choice([
            "Nigeria is home to vibrant fashion styles! 🇳🇬",
            "Explore authentic Nigerian fabrics and clothing here! 👗",
            "We bring you the best of Nigerian fashion! 🛍️"
        ])
    
    if "style" in user_message or "trendy" in user_message or "shopping" in user_message:
        return random.choice([
            "Looking for trendy outfits? I can help! 😎",
            "Let’s find your next stylish look! 👗🥿",
            "I can show you products by category, price, or type! 🛍️"
        ])
    
    # ---------- SHOW CATEGORIES ----------
    if "category" in user_message or "categories" in user_message:
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()
        reply = "Our product categories are:\n"
        for c in categories:
            reply += f"- {c['name']}\n"
        reply += "\nType a category name to view products."
        return reply
    
    # ---------- CATEGORY DETECTION ----------
    cursor.execute("SELECT name FROM categories")
    categories = [c['name'] for c in cursor.fetchall()]
    for category in categories:
        if category.lower() in user_words:
            items = get_products_by_category(category)
            return format_products(items)
    
    # ---------- PRICE QUERY ----------
    if "under" in user_message or "price" in user_message:
        max_price = 20000  # default
        for word in user_words:
            if word.isdigit():
                max_price = float(word)
                break
        items = get_products_by_price(max_price)
        return format_products(items)
    
    # ---------- SHOW ALL PRODUCTS ----------
    if "product" in user_message or "clothes" in user_message:
        cursor.execute("SELECT name, price, stock FROM products")
        products = cursor.fetchall()
        return format_products(products)
    
    # ---------- GOODBYE ----------
    if "bye" in user_message or "goodbye" in user_message:
        return "Thank you for visiting our store! 👋"
    
    # ---------- DEFAULT RESPONSE ----------
    return (
        "Sorry, I didn't understand that. 😅\n"
        "You can ask about:\n"
        "- categories (men/women/footwear/accessories/fabrics/traditional wear)\n"
        "- products under a certain price\n"
        "- show all products\n"
        "- say hi, hello, how are you, fashion, Nigeria, trendy, or ask me for a joke! 😄"
    )

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    bot_reply = chatbot_response(user_message)
    log_chat(user_message, bot_reply)
    return jsonify({"reply": bot_reply})

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
