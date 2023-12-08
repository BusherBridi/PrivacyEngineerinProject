from flask import Flask, render_template
import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure the PostgreSQL connection
db_params = {
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Function to create a connection to the PostgreSQL database
def create_connection():
    connection = psycopg2.connect(**db_params)
    return connection

@app.route('/')
def home():
    # Example: Fetch data from the database
    connection = create_connection()
    cursor = connection.cursor()

    # Example query
    cursor.execute('SELECT * FROM person')
    data = cursor.fetchall()
    print(data)

    connection.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
