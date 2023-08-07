from flask import Blueprint, jsonify, request
from connection.connection import create_connection
bp = Blueprint('favorites', __name__)

@bp.route('/api/addtofavorites', methods=['POST'])
def add_to_favorites():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    # Perform validation on user_id and product_id
    if user_id is None or product_id is None:
        return jsonify({'error': 'user_id and product_id are required'}), 400

    # Create a connection to the database
    connection = create_connection()

    try:
        # Create a cursor
        cursor = connection.cursor()

        # Check if the user_id and product_id combination already exists in the favorites table
        cursor.execute('SELECT id FROM favorites WHERE user_id = %s AND product_id = %s', (user_id, product_id))
        result = cursor.fetchone()

        if result:
            # If the combination already exists, return an error
            return jsonify({'error': 'Product is already added to favorites'}), 400
        else:
            # If the combination does not exist, insert the data into the favorites table
            cursor.execute('INSERT INTO favorites (user_id, product_id) VALUES (%s, %s)', (user_id, product_id))
            connection.commit()

            return jsonify({'message': 'Product added to favorites successfully'}), 200

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/getfavorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    # Create a connection to the database
    connection = create_connection()

    try:
        # Create a cursor
        cursor = connection.cursor()

        # Get the favorites for the specific user_id
        cursor.execute('SELECT products.id, products.name, products.cost, products.description, products.type, '
                       'products.created_by, products.image, products.color, products.size, products.is_printed '
                       'FROM products '
                       'INNER JOIN favorites ON products.id = favorites.product_id '
                       'WHERE favorites.user_id = %s', (user_id,))
        favorites = cursor.fetchall()

        # Transform favorites into a list of dictionaries
        favorite_list = [{'id': favorite[0], 'name': favorite[1], 'cost': favorite[2], 'description': favorite[3],
                          'type': favorite[4], 'created_by': favorite[5], 'image': favorite[6],
                          'color': favorite[7], 'size': favorite[8], 'is_printed': favorite[9]} for favorite in favorites]

        # Return the list of favorites for the given user_id as JSON response
        return jsonify({'favorites': favorite_list})
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


@bp.route('/api/unlike/<int:user_id>/<int:product_id>', methods=['DELETE'])
def unlike_product(user_id, product_id):
    # Remove the product with product_id from the favorites list for the user with user_id
    # Perform the necessary operations to remove the item from the favorites list in your database
    # Return an appropriate response, e.g., 200 OK or 404 Not Found if the product was not found in the favorites list

    # Sample implementation assuming you have a database
    connection = create_connection()
    try:

        cursor = connection.cursor()

        # Check if the product is in the favorites list for the user
        cursor.execute('SELECT 1 FROM favorites WHERE user_id = %s AND product_id = %s', (user_id, product_id))
        result = cursor.fetchone()

        if result:
            # Product is in the favorites list, remove it
            cursor.execute('DELETE FROM favorites WHERE user_id = %s AND product_id = %s', (user_id, product_id))
            connection.commit()
            return jsonify({'message': 'Product successfully removed from favorites.'}), 200
        else:
            # Product was not found in the favorites list
            return jsonify({'error': 'Product not found in favorites.'}), 404
    except Exception as e:
        # Handle any exceptions or errors that may occur during the process
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

