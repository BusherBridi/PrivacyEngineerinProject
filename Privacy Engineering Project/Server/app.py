from flask import Flask, session, render_template, request, jsonify
import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib
import pandas as pd
from faker import Faker
import random
import time
app = Flask(__name__)

# Configure the PostgreSQL connection
# db_params = {
#     'user': 'postgres',
#     'password': 'password',
#     'host': '172.233.158.219',
#     'port': '5432'
# }
db_params = {
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

TARGET_K_SCORE = 2
TARGET_DELTA_SCORE = 0.5
duration = 0
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
        print("failure here")
        return render_template("error.html")

    else:
        try:
            
            cursor.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)", (email, username, hashedPassword))
            connection.commit()
            connection.close()
        except Exception as error:
            print("failure here 2")
            errorMSG = error.args[0]
            print(errorMSG)
            return render_template("error.html", error=errorMSG)
        else:
            # session["logged_in"] = True
            # userInfo = cursor.execute("SELECT * FROM users WHERE username =:username",{"username":username}).fetchone()
            # session["user_info"] = {"user_id": userInfo.id, "firstName": userInfo.firstname}
            return render_template("userCreationComplete.html")

@app.route('/LoginPage')
def LoginPage():
    return render_template('login.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    connection = create_connection()
    cursor = connection.cursor()
    username = str(request.form.get("username").upper())
    password = str(request.form.get("password"))
    passwordHash = hashlib.sha256()
    passwordHash.update(password.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())
    user_data = cursor.execute("SELECT * FROM users WHERE upper(username) = %s AND password = %s", (username, hashedPassword))
    if cursor.rowcount == 1:
        # Username and password match
        matched_user = cursor.fetchone()
        print(f"User found: {matched_user}")
        return render_template("userpage.html", user_data=matched_user)
    else:
        # No match found
        print("Username and password do not match.")
        return("no user found")

    return render_template("error.html")

@app.route('/update_user', methods = ["POST"])
def update_user():
    return 0

@app.route('/submitComplaint', methods = ["POST", "GET"])
def submitComplaint():
    return render_template('complaintSubmitPage.html')



def calculateKScore(data, qID):
    equivalence_classes = data[qID].copy().drop_duplicates()
    equivalence_classes["k"] = data.groupby(qID)[qID[0]].transform('count')
    equivalence_classes = equivalence_classes.reset_index(drop=True)

    k = equivalence_classes["k"].min()
    
    return k, equivalence_classes
def generate_zip_code():
    return f"{random.randint(99900, 99999)}"

def generate_dummy_data(num_entries):
    zip_codes = [generate_zip_code() for _ in range(20)]
    fake = Faker()

    data = []
    for _ in range(num_entries):
        full_name = fake.name()
        name_parts = full_name.split(maxsplit=1)

        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        entry = {
            'email': f"{first_name.lower()}{last_name.lower()}@example.com",
            'full_name': full_name,
            'zip_code': fake.random_element(elements=zip_codes),
            'gender': fake.random_element(elements=('Male', 'Female', 'Other')),
            'social_security': fake.random_int(min=100000000, max=999999999),
            'age': fake.pyint(min_value=18, max_value=99),  # Random age between 18 and 99
            'employee_number': fake.random_int(min=1000, max=9999),
            'department': fake.random_element(elements=('HR', 'IT', 'Product', 'Sales', 'Legal', 'Marketing')),
            'type_of_report': fake.random_element(elements=('General', 'Sexual Harassment', 'Racial Discrimination', 'Gender Discrimination', 'Bullying', 'Whistleblower', 'Workplace Violence', 'Unfair Labor Practices', 'Retaliation', 'Health and Safety Violations', 'Fraud', 'Ethical Violations', 'Privacy Violations', 'Environmental Violations')),
            'phone_number': fake.phone_number()[:10],
            'is_true': False
        }
        data.append(entry)
    return data

def insert_dummy_users(connection, dummy_data):
    cursor = connection.cursor()

    for entry in dummy_data:
        cursor.execute(
            "INSERT INTO personal_info (full_name, zip_code, gender, social_security, age, "
            "employee_number, department, type_of_report, email, phone_number) VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                entry['full_name'], entry['zip_code'], entry['gender'], entry['social_security'],
                entry['age'], entry['employee_number'], entry['department'],
                entry['type_of_report'], entry['email'], entry['phone_number']
            )
        )
    connection.commit()
    cursor.close() 
    return 0

def insert_dummy_reports(connection, dummy_data):
    cursor = connection.cursor()

    for entry in dummy_data:
        cursor.execute(
            "INSERT INTO reports (full_name, zip_code, gender, social_security, age, "
            "employee_number, department, type_of_report, email, phone_number, is_true) VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                entry['full_name'], entry['zip_code'], entry['gender'], entry['social_security'],
                entry['age'], entry['employee_number'], entry['department'],
                entry['type_of_report'], entry['email'], entry['phone_number'], entry['is_true']
            )
        )
    connection.commit()
    cursor.close() 
    return 0


@app.route('/sendComplaint', methods = ["POST", "GET"])
def sendComplaint():
    start_time = time.time()
    connection = create_connection()
    cursor = connection.cursor()
    fullName = str(request.form.get("fullName").upper())
    zipCode = str(request.form.get("zipCode"))
    gender = str(request.form.get("gender"))
    socialSecurityNumber = str(request.form.get("ssn"))
    age = str(request.form.get("age"))
    employeeNumber = str(request.form.get("employeeNumber"))
    department = str(request.form.get("department"))
    typeOfReport = str(request.form.get("typeOfReport"))
    email = str(request.form.get("email"))
    phoneNumber = str(request.form.get("phoneNumber"))
    isTrue = True

    fetchQuery = pd.read_sql_query("SELECT * FROM reports", connection)
    connection.commit()
    df = pd.DataFrame(fetchQuery, columns=["zip_code", "gender", "age", "department", "type_of_report"])
    kScore, eqv_classes = calculateKScore(df, ["gender", "department", "type_of_report"])
    print("kscore = " + str(kScore))
    
    while kScore < TARGET_K_SCORE:
        fakeData = generate_dummy_data(1)
        insert_dummy_reports(connection, fakeData)
        fetchQuery = pd.read_sql_query("SELECT * FROM reports", connection)
        connection.commit()
        df = pd.DataFrame(fetchQuery, columns=["zip_code", "gender", "age", "department", "type_of_report"])
        kScore, eqv_classes = calculateKScore(df, ["gender", "department", "type_of_report"])
        print("Inserted data: " + str(fakeData))
        print("Current KScore = " + str(kScore))

    

    # Delta Presence:
    # calculate existing delta presence for speicfic employee's qID:
    cursor.execute("SELECT COALESCE(COUNT(*), 0) as row_count FROM personal_info GROUP BY gender, department, type_of_report HAVING COUNT(*) > 1;")
    result = cursor.fetchone()
    print(result)
    personal_info_count = result[0] if result is not None else 0
    cursor.execute("SELECT COALESCE(COUNT(*), 0) as row_count FROM reports GROUP BY gender, department, type_of_report HAVING COUNT(*) > 1;")
    result = cursor.fetchone()
    reports_count = result[0] if result is not None else 0
    current_delta_score = 1
    if(personal_info_count == 0):
        current_delta_score = 1
    else:
        current_delta_score = reports_count/personal_info_count
    while current_delta_score > TARGET_DELTA_SCORE:
        fakeData = generate_dummy_data(1)
        insert_dummy_users(connection, fakeData)
        print("Inserting fake users")

        # Query for personal_info
        cursor.execute("SELECT COALESCE(COUNT(*), 0) as row_count FROM personal_info GROUP BY gender, department, type_of_report HAVING COUNT(*) > 1;")
        personal_info_result = cursor.fetchone()
        personal_info_count = personal_info_result[0] if personal_info_result is not None else 0

        # Query for reports
        cursor.execute("SELECT COALESCE(COUNT(*), 0) as row_count FROM reports GROUP BY gender, department, type_of_report HAVING COUNT(*) > 1;")
        reports_result = cursor.fetchone()
        reports_count = reports_result[0] if reports_result is not None else 0

        if personal_info_count == 0:
            current_delta_score = 0
        else:
            current_delta_score = reports_count / personal_info_count

        print("Current delta: " + str(current_delta_score))

    cursor.execute("INSERT INTO reports (full_name, zip_code, gender, social_security, age, employee_number, department, type_of_report, email, phone_number, is_true) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", (fullName, zipCode, gender, socialSecurityNumber, age, employeeNumber, department, typeOfReport, email, phoneNumber, isTrue))
    cursor.execute("INSERT INTO personal_info (full_name, zip_code, gender, age, department, social_security) VALUES (%s, %s, %s, %s, %s, %s)", (fullName, zipCode, gender, age, department, socialSecurityNumber))

    connection.commit()
    connection.close()

    end_time = time.time()
    duration = end_time - start_time
    print("DURATION: " + str(duration))
    return render_template("index.html")

@app.route('/results')
def results():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reports;")
    reports_data = cursor.fetchall()
    # today = datetime.today()
    cursor.execute("SELECT * FROM personal_info;")
    personal_info = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM reports WHERE is_true = true;")
    true_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM reports WHERE is_true = false;")
    false_count = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    total_count = true_count + false_count
    ratio = true_count / total_count if total_count > 0 else 0
    ratio = round(ratio, 3)
    # print(table_data[0])
    return render_template('results.html',reports_data = reports_data, personal_info=personal_info, ratio=ratio, kScore = TARGET_K_SCORE, delta = TARGET_DELTA_SCORE, time = duration)

def delta_Presence_of_Individual(identities, identities_row_id, published_table, quasi_identifiers):
    cnt_identities = identities[quasi_identifiers][identities[quasi_identifiers] == identities.loc[identities_row_id, quasi_identifiers]].dropna().shape[0]
    cnt_published_table = published_table[quasi_identifiers][published_table[quasi_identifiers] == identities.loc[identities_row_id, quasi_identifiers]].dropna().shape[0]
    if cnt_identities > 0:
        delta = cnt_published_table / cnt_identities
    else:
        delta = 0.0
    return delta

@app.route('/calculate_delta', methods=['POST'])
def calculate_delta():
    try:
        # Get data from the request
        request_data = request.json
        identities_data = request_data['identities']
        identities_row_id = request_data['identities_row_id']
        published_table_data = request_data['published_table']
        quasi_identifiers = request_data['quasi_identifiers']

        # Convert data to pandas DataFrames
        identities = pd.DataFrame(identities_data)
        published_table = pd.DataFrame(published_table_data)

        # Calculate delta
        delta_value = delta_Presence_of_Individual(identities, identities_row_id, published_table, quasi_identifiers)

        # Return the result
        return jsonify({'delta': delta_value})

    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@app.route('/test')
def render():
        return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
