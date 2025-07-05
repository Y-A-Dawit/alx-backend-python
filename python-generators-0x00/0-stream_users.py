import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        user='root',
        password='your_password',
        host='localhost',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
