from flask import Flask, render_template

app = Flask( __name__)

@app.route('/')
def home():
    # return "Hello world"
    return render_template("index.html")


@app.route('/about')
def about():
    # return "Hello world"
    return render_template("about.html")


# if __name__ == "__main__":
#     print("app is running")
#     # app.run(debug=True)
#     app.run(host="0.0.0.0", port=5000, debug=True)
   
