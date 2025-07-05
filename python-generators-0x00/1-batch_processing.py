import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        user='root',
        password='your_password',
        host='localhost',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch  # yield here, NOT return
            batch = []
    if batch:
        yield batch  # yield remaining batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user['age']) > 25:
                print(user)
