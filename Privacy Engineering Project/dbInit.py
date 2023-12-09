import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker


# Configure the PostgreSQL connection
db_params = {
    'user': 'postgres',
    'password': 'password',
    'host': '172.233.158.219',
    'port': '5432'
}




# Function to create a connection to the PostgreSQL database
def create_connection():
    connection = psycopg2.connect(**db_params)
    return connection


def create_users_table():
    connection = create_connection()
    cursor = connection.cursor()
    output = cursor.execute('''CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
    );''')
    connection.close()
    return output

print(create_users_table())





'''  # Example: Fetch data from the database
    connection = create_connection()
    cursor = connection.cursor()

    # Example query
    cursor.execute('SELECT * FROM person')
    data = cursor.fetchall()
    print(data)
    connection.close()
    '''