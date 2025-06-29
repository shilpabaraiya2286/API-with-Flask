from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage
users = {}

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the User Management API"}), 200

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# Get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user}), 200
    return jsonify({"error": "User not found"}), 404

# Create a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data.get('id')
    name = data.get('name')
    email = data.get('email')

    if not user_id or not name or not email:
        return jsonify({"error": "Missing user ID, name, or email"}), 400
    if user_id in users:
        return jsonify({"error": "User already exists"}), 400

    users[user_id] = {"name": name, "email": email}
    return jsonify({"message": "User created successfully"}), 201

# Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if name:
        users[user_id]['name'] = name
    if email:
        users[user_id]['email'] = email

    return jsonify({"message": "User updated successfully"}), 200

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
