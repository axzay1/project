import psycopg2

def create_connection():
    # Database connection parameters
    host = 'localhost'  # Replace with your database host
    port = '5432'  # Replace with your database port
    dbname = 'iq100'  # Replace with your database name
    user = 'postgres'  # Replace with your database username
    password = 'Akshay007'  # Replace with your database password

    # Create a connection
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

    return connection
