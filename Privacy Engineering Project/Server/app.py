from flask import Flask, session, render_template, request, jsonify
import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib

app = Flask(__name__)

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

#Privacy Algorithims








'''  # Example: Fetch data from the database
    connection = create_connection()
    cursor = connection.cursor()

    # Example query
    cursor.execute('SELECT * FROM person')
    data = cursor.fetchall()
    print(data)
    connection.close()
    '''
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
     return render_template('signup.html')

@app.route("/userCreationComplete", methods=["POST", "GET"])
def userCreationComplete():
    connection = create_connection()
    cursor = connection.cursor()
    print(request.form)
    email = str(request.form.get("email"))
    username = str(request.form.get("username").upper())
    password = str(request.form.get("password"))
    passwordHash = hashlib.sha256()
    passwordHash.update(password.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest()) #I have no clue why I have to do this line
    if(len(password) < 8):
        errorMSG = "Password must be at least 8 characters long"
        return render_template("error.html", error = errorMSG)
    if(not email or not username or not password):
        return render_template("error.html")

    else:
        try:
            
            cursor.execute("INSERT INTO users (email, username, password) VALUES (:email, :username, :password)",
                       { "email": email, "username": username, "password": hashedPassword})
            cursor.commit()
        except Exception as error:
            errorMSG = error.args[0]
            return render_template("error.html", error=errorMSG)
        else:
            # session["logged_in"] = True
            # userInfo = cursor.execute("SELECT * FROM users WHERE username =:username",{"username":username}).fetchone()
            # session["user_info"] = {"user_id": userInfo.id, "firstName": userInfo.firstname}
            return render_template("userCreationComplete.html")

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/results')
def results():
     return render_template('results.html')


@app.route('/test')
def render():
        return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
