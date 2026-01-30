from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import random

# ---------------- LOAD ENVIRONMENT VARIABLES ----------------
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
    """Format products for chatbot display."""
    if not items:
        return "No products found."
    reply = "Available products:\n"
    for item in items:
        reply += f"- {item['name']} | ₦{item['price']:.2f} | Stock: {item['stock']}\n"
    return reply

def get_products_by_category(category_name):
    """Return products for a given category."""
    query = """
        SELECT p.name, p.price, p.stock
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE c.name = %s
    """
    cursor.execute(query, (category_name,))
    return cursor.fetchall()

def get_products_by_price_range(range_name):
    """Return products within a price range."""
    query = """
        SELECT p.name, p.price, p.stock
        FROM products p
        JOIN price_ranges pr
        WHERE p.price >= pr.min_price
        AND (p.price <= pr.max_price OR pr.max_price IS NULL)
        AND pr.range_name = %s
    """
    cursor.execute(query, (range_name,))
    return cursor.fetchall()

def get_products_under_price(max_price):
    """Return products under a specific price (fallback numeric)."""
    query = "SELECT name, price, stock FROM products WHERE price <= %s"
    cursor.execute(query, (max_price,))
    return cursor.fetchall()

def log_chat(user_msg, bot_msg):
    """Log user and bot messages into database."""
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
    if user_message in ["hi", "hello", "hey", "hiya", "howdy", "greetings", 
                        "good morning", "good afternoon", "good evening"]:
        return random.choice([
            "Hello! Welcome to our Nigerian fashion store 👗",
            "Hi there! How can I help you shop today?",
            "Hey! Looking for something trendy today?",
            "Good day! Ready to explore the latest fashion styles?",
            "Welcome! Let's find you something fabulous to wear ✨",
            "Hi! We have some amazing outfits you might love!",
            "Hey there! Are you in the mood for some fashion inspiration?",
            "Hello! Step in and discover our exclusive collections!",
            "Hi! Let's make your wardrobe shine today 🌟",
            "Greetings! Ready to elevate your style game?"
        ])

    # ---------- SMALL TALK ----------
# ---------- SMALL TALK ----------
    if any(phrase in user_message for phrase in ["how are you", "how's it going", "how do you do", "how are things", "what's up"]):
        return random.choice([
            "I'm doing well, thank you! How about you? 😊",
            "All good here! Ready to help you find fashion items 👗",
            "I'm fine! Excited to help you shop for clothes today! 😄",
            "Doing great! Are you in the mood for some fashion browsing? 😎",
            "All good! Let’s find something stylish for you today! 👗",
            "I’m doing awesome! What about you? 😄"
        ])

    if "who are you" in user_message or "your name" in user_message.lower():
        return random.choice([
            "I'm your AI fashion sales assistant 🤖",
            "I help you find clothes, shoes, and accessories!",
            "You can call me FashionBot!",
            "I'm your style guide for all things trendy! 👗✨",
            "Think of me as your personal fashion genie 🧞‍♀️",
            "Your fashion assistant, always ready to help you slay! 💃",
            "I'm the one who helps you turn heads with your outfits 😉",
            "Your virtual wardrobe buddy, at your service!",
            "I keep up with Nigerian fashion trends so you don’t have to!",
            "Your friendly fashion AI, making shopping fun and easy!"
        ])

    if user_message in ["thanks", "thank you", "thank", "thx", "tnks", "tnk", "done", "bye", "appreciate it"]:
        return random.choice([
            "You're welcome! 😄",
            "No problem! Happy shopping! 😊",
            "Glad I could help! 👗",
            "Anytime! Let me know if you need more fashion tips ✨",
            "My pleasure! Your style is my priority 💖",
            "Always here to help you slay! 💃"
        ])

    message = user_message.lower()
    
    happy_keys = ["happy", "joyful", "excited", "great", "good"]
    sad_keys = ["sad", "down", "unhappy", "bored", "meh"]

    if any(key in message for key in happy_keys):
        return random.choice([
            "Yay! Love that you're feeling happy! 😄 Fashion makes it even better! 👗",
            "Awesome! Your mood and style are on point today! ✨",
            "Feeling great? Let's find you an outfit that matches your vibe! 💃",
            "Happiness looks good on you, but a new outfit can make it even better! 😎"
        ])
    elif any(key in message for key in sad_keys):
        return random.choice([
            "Cheer up! Maybe a new outfit will lift your spirits 😊",
            "Fashion always brightens the day! 👗",
            "Feeling down? Let’s find something trendy to make you smile! ✨",
            "Don’t worry! A little shopping therapy can work wonders 💖"
        ])

    message = user_message.lower()
    help_keys = ["what can you do", "help", "assist", "services", "guide me", "how can you help"]

    if any(key in message for key in help_keys):
        return random.choice([
            "I can help you browse our product categories, check prices, and find clothing for men, women, and more 👗",
            "Looking for the latest Nigerian fashion trends? I can guide you to outfits, shoes, and accessories! ✨",
            "I assist you in finding the perfect look—whether casual, party, or traditional wear!",
            "Need style tips or outfit ideas? I’ve got you covered! 💃",
            "I can help you shop smart, explore collections, and find trendy pieces for any occasion!"
        ])

    message = user_message.lower()

    joke_keys = ["joke", "jokes", "tell me a joke"]
    laugh_keys = ["haha", "lol", "lmao", "hehe", "rofl"]

    # If user asks for a joke
    if any(key in message for key in joke_keys):
        return random.choice([
            "Why did the belt go to jail? Because it held up a pair of pants! 😆",
            "I would tell you a joke about shoes, but it might be too soleful! 😅",
            "Why did the shirt go to school? It wanted to be a little brighter! 👕",
            "Why did the scarf break up with the coat? It felt tied down! 🧣",
            "Why don’t shoes ever get lost? Because they always follow their soles! 👟",
            "I know a tailor joke, but it’s a bit of a stretch! ✂️😄"
        ])
    
    # If user is laughing
    elif any(key in message for key in laugh_keys):
        return random.choice([
            "😂 Glad you liked it!",
            "😄 Fashion humor always hits!",
            "Haha! I knew that one would make you smile 😎",
            "🤣 Laughter is the best accessory, after a nice outfit of course!"
        ])
    

    message = user_message.lower()
    
    fashion_keys = ["fashion", "nigeria", "trendy", "clothes", "outfits", "style", "attire", "wardrobe"]

    if any(key in message for key in fashion_keys):
        return random.choice([
            "Yes! We have the latest Nigerian fashion styles 👗",
            "Looking trendy? I can show you clothes, footwear, and accessories! 😎",
            "Our fashion items are perfect for Nigerian styles 🇳🇬",
            "From casual wear to party outfits, we’ve got you covered! ✨",
            "Step up your style game with our newest collections 💃",
            "Want traditional or modern Nigerian styles? I can help you find both! 👘",
            "I can guide you through outfits that will make heads turn! 😍"
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
    categories = [c['name'].lower() for c in cursor.fetchall()]
    for category in categories:
        if category in user_words:
            items = get_products_by_category(category)
            return format_products(items)

    # ---------- PRICE RANGE DETECTION ----------
    cursor.execute("SELECT range_name FROM price_ranges")
    ranges = [r['range_name'].lower() for r in cursor.fetchall()]
    for r in ranges:
        if r in user_words:
            items = get_products_by_price_range(r.capitalize())
            return format_products(items)

    # ---------- PRICE QUERY (numeric) ----------
    for word in user_words:
        if word.isdigit():
            max_price = float(word)
            items = get_products_under_price(max_price)
            return format_products(items)

    # ---------- SHOW ALL PRODUCTS ----------
    if "product" in user_message or "clothes" in user_message or "wear" in user_message:
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
    print("STARTING APP ...")
    app.run(debug=True, port=5001)
