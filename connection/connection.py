from xmlrpc.client import SERVER_ERROR
import psycopg2

# CONNECTION TO LOCALHOST DB SERVER_ERROR

# def create_connection():
#     # Database connection parameters
#     host = 'localhost'  # Replace with your database host
#     port = '5432'  # Replace with your database port
#     dbname = 'iq100'  # Replace with your database name
#     user = 'postgres'  # Replace with your database username
#     password = 'Akshay007'  # Replace with your database password

#     # Create a connection
#     connection = psycopg2.connect(
#         host=host,
#         port=port,
#         dbname=dbname,
#         user=user,
#         password=password
#     )

#     return connection

# CONNECTION TO AWS DB SERVER


def create_connection():
    # Database connection parameters
    host = 'database-1.cqm57ku6cupz.us-west-2.rds.amazonaws.com'   # Replace with your database host
    port = '5432'  # Replace with your database port
    dbname = 'iq100'  # Replace with your database name
    user = 'root'  # Replace with your database username
    password = 'Agrifi1234'  # Replace with your database password

    # Create a connection
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

    return connection