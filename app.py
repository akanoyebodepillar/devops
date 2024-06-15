from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Initial list of users
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# Route for the home page
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Management</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 300px;
                margin-bottom: 20px;
            }
            h1, h2 {
                font-size: 24px;
                margin-bottom: 20px;
                text-align: center;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input[type="text"], input[type="number"], input[type="submit"] {
                width: 100%;
                padding: 10px;
                margin: 5px 0 20px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background: #e0e0e0;
                margin: 5px 0;
                padding: 10px;
                border-radius: 3px;
                text-align: center;
            }
            .error {
                color: red;
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Add a New User</h1>
            <form action="/users" method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <input type="submit" value="Add User">
            </form>
        </div>

        <div class="container">
            <h2>Get User by ID</h2>
            <form action="/get_user" method="post">
                <label for="user_id">User ID:</label>
                <input type="number" id="user_id" name="user_id" required>
                <input type="submit" value="Get User">
            </form>
            {% if user %}
                <h2>Found User</h2>
                <ul>
                    <li>{{ user['name'] }}</li>
                </ul>
            {% elif error %}
                <div class="error">{{ error }}</div>
            {% endif %}
        </div>

        <div class="container">
            <h2>Current Users</h2>
            <ul>
                {% for user in users %}
                    <li>{{ user['name'] }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, users=users)

# Route to handle both getting all users and adding a new user
@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        # Return the list of users
        return jsonify(users)
    
    if request.method == 'POST':
        # Get the new user data from the form
        new_user = {"name": request.form['name']}
        # Assign a new ID to the new user
        if users:
            new_user["id"] = users[-1]["id"] + 1
        else:
            new_user["id"] = 1
        # Add the new user to the list
        users.append(new_user)
        # Redirect back to home
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta http-equiv="refresh" content="0; url=/" />
        </head>
        <body>
            Redirecting...
        </body>
        </html>
        """)

# Route to get a specific user by ID and display in HTML
@app.route('/get_user', methods=['POST'])
def get_user_by_id():
    user_id = int(request.form['user_id'])
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta http-equiv="refresh" content="0; url=/" />
        </head>
        <body>
            Redirecting...
        </body>
        </html>
        """, user=user, users=users)
    else:
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta http-equiv="refresh" content="0; url=/" />
        </head>
        <body>
            Redirecting...
        </body>
        </html>
        """, error="User not found", users=users)

# Route to get a specific user by ID and return JSON
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)