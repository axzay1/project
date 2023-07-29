from flask import Blueprint, request, jsonify
from connection.connection import create_connection

bp = Blueprint('user', __name__)

@bp.route('/api/getuser', methods=['GET'])
def get_users():
    # Create a connection
    connection = create_connection()

    # Create a cursor
    cursor = connection.cursor()

    try:
        # Execute a query to retrieve users
        cursor.execute('SELECT * FROM users')

        # Fetch the query results
        users = cursor.fetchall()

        # Transform users into a list of dictionaries
        user_list = [{'id': user[0], 'name': user[1], 'email': user[2]} for user in users]

        # Return the list of users as JSON response
        return jsonify({'users': user_list})
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/user', methods=['POST'])
def create_user():
    # Extract user data from the request
    data = request.get_json()
    name = data['name']
    email = data['email']

    # Create a connection
    connection = create_connection()

    # Create a cursor
    cursor = connection.cursor()

    try:
        # Execute a query to insert a new user
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))

        # Commit the transaction
        connection.commit()

        # Return the created user as JSON response
        return jsonify({'message': 'User created successfully'})
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/login', methods=['POST'])
def login():
    # Extract email and password from the request
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Create a connection
    connection = create_connection()

    # Create a cursor
    cursor = connection.cursor()

    try:
        # Execute a query to retrieve the user with the given email
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))

        # Fetch the query result
        user = cursor.fetchone()

        if user:
            # Check if the provided password matches the stored password
            if password == user[7]:  # Assuming the password is at index 3 in the user tuple
                # Transform the user into a dictionary
                user_dict = {'id': user[0], 'name': user[1], 'email': user[2]}

                # Return the user as JSON response
                return jsonify({'user': user_dict}), 200
            else:
                # Return an error message if password is incorrect
                return jsonify({'message': 'Incorrect password'}), 401
        else:
            # Return an error message if user not found
            return jsonify({'message': 'User not found'}), 404
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
    
@bp.route('/api/register', methods=['POST'])
def register():
    # Extract data from the request
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Create a connection
    connection = create_connection()

    # Create a cursor
    cursor = connection.cursor()

    try:
        # Check if the email is already registered
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            # Return an error message if the email is already registered
            return jsonify({'message': 'Email already registered'}), 409
        else:
            # Insert the new user data into the 'users' table
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                           (name, email, password))

            # Commit the changes to the database
            connection.commit()

            # Return a success message
            return jsonify({'message': 'Registration successful'}), 201

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()