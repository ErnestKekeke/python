from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# home route
@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        return "Nothing from home !!!"

# about route
@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':
        return render_template('about.html')
    else:
        return "Nothing from about !!!"


@app.route('/contact', methods=['GET'])
@app.route('/contact/<name>/<int:age>', methods=['GET'])
def contact(name='unknown', age=0):
    return f"name: {name}, age: {age}"



# Sample data: 3 posts
data = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the first post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'Here is the second post.'},
    {'id': 3, 'title': 'Third Post', 'content': 'And this is the third post.'},
]

# GET for all posts
@app.route('/posts', methods=['GET'])
def all_posts():
    posts = data
    # return posts
    return jsonify(posts) # import to always use this

# GET for a single posts
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = next((p for p in data if p['id'] == id), None)
    if(post):
        return jsonify(post)
    else:
        return jsonify({'error': f'No post with id: {id}'}), 404
    

# Create a new Post .................................................
@app.route('/posts', methods=['POST'])
def create_post():
    # Try to read JSON first
    body = request.get_json(silent=True)  # silent=True prevents exceptions

    # If no JSON, try form data
    if not body:
        body = request.form.to_dict()  # convert ImmutableMultiDict to normal dict

    # Validate required fields
    if 'title' not in body or 'content' not in body:
        return jsonify({'error': 'title and content are required'}), 400

    # Create new post
    new_post = {
        'id': max(p['id'] for p in data) + 1 if data else 1,
        'title': body['title'],
        'content': body['content']
    }
    data.append(new_post)
    return jsonify(new_post), 201


# PUT Request ... method 1 .......................................
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = next((p for p in data if p['id'] == id), None)

    if not post:
        return jsonify({'error': f'No post with id: {id}'}), 404
    
    body = request.get_json()
    # Update only provided fields
    if 'title' in body:
        post['title'] = body['title']
    if 'content' in body:
        post['content'] = body['content']

    return jsonify(post), 200


# # PUT Request ... Method 2, using form data
# @app.route('/posts/<int:id>', methods=['PUT'])
# def update_post(id):
#     post = next((p for p in data if p['id'] == id), None)

#     if not post:
#         return jsonify({'error': f'No post with id: {id}'}), 404

#     title = request.form.get('title')
#     content = request.form.get('content')

#     if title:
#         post['title'] = title
#     if content:
#         post['content'] = content

#     return jsonify(post), 200


# Delete Request:

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global data  # required if we reassign the list
    post = next((p for p in data if p['id'] == id), None)

    if not post:
        return jsonify({'error': f'No post with id: {id}'}), 404

    # Remove the post from the list
    data = [p for p in data if p['id'] != id]

    return jsonify({'message': f'Post {id} deleted successfully'}), 200



# run app
if __name__ == '__main__':
    print("Starting App Running")
    app.run(debug=True, port=5001)

