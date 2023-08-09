from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from connection.connection import create_connection
bp = Blueprint('products', __name__)
from sqlalchemy import or_, and_
from models.product import Product  

@bp.route('/api/getproducts', methods=['GET'])
@cross_origin()
def get_products():
    # Create a connection
    connection = create_connection()

    # Create a cursor
    cursor = connection.cursor()

    try:
        # Execute a query to retrieve products
        cursor.execute('SELECT * FROM products')

        # Fetch the query results
        products = cursor.fetchall()

        # Transform products into a list of dictionaries
        product_list = [{'id': product[0], 'name': product[1], 'cost': product[2], 'description': product[3], 'type': product[4], 'created_by': product[5], 'image': product[7], 'color': product[8], 'size' : product[8], 'is_printed' : product[9]} for product in products]

        # Return the list of products as JSON response
        return jsonify({'products': product_list})
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/getproducttype/<string:product_type>', methods=['GET'])
@cross_origin()
def get_products_by_type(product_type):
    try:    
        # Create a connection to the database
        connection = create_connection()

        # Create a cursor
        cursor = connection.cursor()

        # Define the SQL query to fetch products by type
        query = "SELECT * FROM products WHERE type = %s;"

        # Execute the query with the product_type as a parameter
        cursor.execute(query, (product_type,))

        # Fetch all the rows and store them in a variable
        products = cursor.fetchall()

        # Transform products into a list of dictionaries
        product_list = [{'id': product[0], 'name': product[1], 'cost': product[2], 'description': product[3], 'type': product[4], 'created_by': product[5], 'image': product[7]} for product in products]

        # Return the list of products with the given type as JSON response
        return jsonify({'products': product_list})
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/filter', methods=['GET'])
@cross_origin()
def filter_products():
    # Get query parameters from the request
    connection = create_connection()

    # Create a cursor
    cursor = connection.cursor()

    try:
        # Get the query parameters from the request
        product_type = request.args.get('type')
        colors = request.args.get('color')
        sizes = request.args.get('size')
        is_printed = request.args.get('is_printed')
        min_cost = request.args.get('min_cost', type=float, default=0.0)
        max_cost = request.args.get('max_cost', type=float, default=1000000.0)  # Use a large value as default

        print("product_type:", product_type)
        print("colors:", colors)
        print("sizes:", sizes)
        print("is_printed:", is_printed)
        print("min_cost:", min_cost)
        print("max_cost:", max_cost)

        # Build the base query
        query = 'SELECT * FROM products WHERE 1=1 '

        # Append filters based on query parameters
        if product_type:
            query += f"AND type = '{product_type}' "

        # Handle multiple colors
        if colors:
            colors = colors.split(',')
            colors_str = "','".join(colors)
            query += f"AND color IN ('{colors_str}') "

        # Handle multiple sizes
        if sizes:
            sizes = sizes.split(',')
            sizes_str = "','".join(sizes)
            query += f"AND size IN ('{sizes_str}') "

        # Handle is_printed parameter
        if is_printed is not None:
            if is_printed.lower() == 'true':
                query += f"AND is_printed = true "
            elif is_printed.lower() == 'false':
                query += f"AND is_printed = false "

        if min_cost is not None:
            query += f"AND cost >= {min_cost} "
        if max_cost is not None:
            query += f"AND cost <= {max_cost} "

        print("Query:", query)

        # Execute the final query
        cursor.execute(query)

        # Fetch the query results
        products = cursor.fetchall()

        # Transform products into a list of dictionaries
        product_list = [{'id': product[0], 'name': product[1], 'cost': product[2], 'description': product[3],
                         'type': product[4], 'created_by': product[5], 'image': product[7],
                         'color': product[8], 'size': product[9], 'is_printed': product[10]} for product in products]

        # Return the list of products as JSON response
        return jsonify({'products': product_list})
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/orders', methods=['POST'])
@cross_origin()
def place_order():
    data = request.get_json()
    user_id = data.get('user_id')
    product_ids = data.get('product_ids')

    # Perform validation on user_id and product_ids
    if user_id is None or not isinstance(product_ids, list):
        return jsonify({'error': 'user_id and product_ids (as a list) are required'}), 400

    # Create a connection to the database
    connection = create_connection()

    try:
        # Create a cursor
        cursor = connection.cursor()

        # Insert the order data into the orders table
        cursor.execute('INSERT INTO orders (user_id) VALUES (%s) RETURNING id', (user_id,))
        order_id = cursor.fetchone()[0]

        print('Inserted order_id:', order_id)  # Debug print
        
        # Insert the product data into the order_products table
        for product_id in product_ids:
            cursor.execute('INSERT INTO order_products (order_id, product_id) VALUES (%s, %s)', (order_id, product_id))
        
        connection.commit()

        return jsonify({'message': 'Order placed successfully'}), 200

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

@bp.route('/api/getorders', methods=['GET'])
@cross_origin()
def get_products_for_user():
    user_id = request.args.get('user_id')
    
    if user_id is None:
        return jsonify({'error': 'user_id is required'}), 400
    
    # Create a connection to the database
    connection = create_connection()

    try:
        # Create a cursor
        cursor = connection.cursor()

        # Execute a query to retrieve products for the given user_id
        cursor.execute('SELECT p.id, p.name, p.cost, p.description, p.type, p.created_by, p.created_at , p.image,  p.color, p.size, p.is_printed '
                       'FROM products p '
                       'INNER JOIN order_products op ON p.id = op.product_id '
                       'INNER JOIN orders o ON op.order_id = o.id '
                       'WHERE o.user_id = %s', (user_id,))

        # Fetch the query results
        products = cursor.fetchall()

        # Transform products into a list of dictionaries
        product_list = [{'id': product[0], 'name': product[1], 'cost': product[2], 'description': product[3],
                         'type': product[4], 'created_by': product[5], 'image': product[7],
                         'color': product[8], 'size': product[9], 'is_printed': product[10]} for product in products]

        # Return the list of products as JSON response
        return jsonify({'products': product_list})

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()