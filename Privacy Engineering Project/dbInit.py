import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from faker import Faker
import random


# Configure the PostgreSQL connection
db_params = {
    'user': 'postgres',
    'password': 'password',
    'host': '172.233.158.219',
    'port': '5432'
}



def generate_zip_code():
    return f"{random.randint(90000, 99999)}"
# Function to create a connection to the PostgreSQL database
def create_connection():
    connection = psycopg2.connect(**db_params)
    return connection


# Modify the 'generate_dummy_data' function to generate related values for username, email, and full name
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
            'username': f"{first_name.lower()}{last_name.lower()}",
            'email': f"{first_name.lower()}{last_name.lower()}@example.com",
            'password': fake.password(),
            'full_name': full_name,
            'zip_code': fake.random_element(elements=zip_codes),
            'gender': fake.random_element(elements=('Male', 'Female', 'Other')),
            'social_security': fake.random_int(min=100000000, max=999999999),
            'date_of_birth': fake.pyint(min_value=18, max_value=99),
            # 'age': fake.pyint(min_value=18, max_value=99),  # Random age between 18 and 99
            'employee_number': fake.random_int(min=1000, max=9999),
            'department': fake.random_element(elements=('HR', 'IT', 'Product', 'Sales', 'Legal', 'Marketing')),
            'type_of_report': fake.random_element(elements=('General', 'Sexual Harassment', 'Racial Discrimination', 'Gender Discrimination', 'Bullying', 'Whistleblower', 'Workplace Violence', 'Unfair Labor Practices', 'Retaliation', 'Health and Safety Violations', 'Fraud', 'Ethical Violations', 'Privacy Violations', 'Environmental Violations')),
            'phone_number': fake.phone_number()[:10]
        }
        data.append(entry)

    return data


# Function to insert dummy data into the 'users' table
def insert_dummy_users(connection, dummy_data):
    cursor = connection.cursor()

    for entry in dummy_data:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (entry['username'], entry['email'], entry['password'])
        )
        cursor.execute(
            "INSERT INTO reports (full_name, zip_code, gender, social_security, date_of_birth, "
            "employee_number, department, type_of_report, email, phone_number) VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                entry['full_name'], entry['zip_code'], entry['gender'], entry['social_security'],
                entry['date_of_birth'], entry['employee_number'], entry['department'],
                entry['type_of_report'], entry['email'], entry['phone_number']
            )
        )
    connection.commit()
    cursor.close()

# Function to get existing emails from the 'users' table
def get_existing_emails(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users")
    emails = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return emails

# Function to insert dummy data into the 'reports' table using existing emails
# def insert_dummy_reports(connection, dummy_data, existing_emails):
#     cursor = connection.cursor()

#     for entry in dummy_data:
#         email = existing_emails.pop(0)
#         cursor.execute(
#             "INSERT INTO reports (full_name, zip_code, gender, social_security, date_of_birth, "
#             "employee_number, department, type_of_report, email, phone_number) VALUES "
#             "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#             (
#                 entry['full_name'], entry['zip_code'], entry['gender'], entry['social_security'],
#                 entry['date_of_birth'], entry['employee_number'], entry['department'],
#                 entry['type_of_report'], email, entry['phone_number']
#             )
#         )

#     connection.commit()
#     cursor.close()

# Usage
if __name__ == "__main__":
    connection = create_connection()

    # Generate and insert dummy data into 'users' table
    dummy_users_data = generate_dummy_data(num_entries=100)
    insert_dummy_users(connection, dummy_users_data)

    # Get existing emails from 'users' table
    # existing_emails = get_existing_emails(connection)

    # Generate and insert dummy data into 'reports' table using existing emails
    # dummy_reports_data = generate_dummy_data(num_entries=10)
    # insert_dummy_reports(connection, dummy_reports_data, existing_emails)

    connection.close()