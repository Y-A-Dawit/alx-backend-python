import mysql.connector
import csv

def connect_db():
    try:
        return mysql.connector.connect(user='root', password='Schadenfreude2190@$', host='localhost')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            user='root',
            password='your_password',
            host='localhost',
            database='ALX_prodev'
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
