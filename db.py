import psycopg2

def get_connect():
    connection = psycopg2.connect(
            host="localhost",      # или IP контейнера
            port="5432",           # порт PostgreSQL
            database="postgres",   # имя базы данных
            user="postgres",       # имя пользователя
            password="123"  # пароль
        )
        
    print("Подключение к PostgreSQL успешно установлено!")
    return connection

def insert_client(cursor,client):
    cursor.execute(
        """
            INSERT INTO clients (id, 
                        name, 
                        diet, 
                        time_interval, 
                        address, 
                        phone, 
                        comment) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING

        """,
        (
           client['id'], 
            client['name'], 
            client['diet'], 
            client['time_interval'], 
            client['address'], 
            client['phone'], 
            client['comment'] 
        )
    )
    return cursor.rowcount

def insert_clients(cursor, done_table):
    added = 0
    skipped = 0
    for client in done_table:
        result = insert_client(cursor, client)
        if result == 1:
            added += 1
        else:
            skipped += 1
    return added, skipped


def save_to_db(done_table):
           
    connection = get_connect()
    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS clients(id integer PRIMARY KEY,
                                            name text,
                                            diet text, 
                                            time_interval text, 
                                            address text, 
                                            phone text, 
                                            comment text)""")
    added, skipped = insert_clients(cursor, done_table)
    connection.commit()
    

    
    # Закрываем соединение
    cursor.close()
    connection.close()
    return {
    "added_count": added,
    "skipped_count": skipped,
    "total_count": len(done_table)
}
        
    

def find_by_id(id):
    connection = get_connect()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM clients WHERE id = %s
        """,
        (id,)
    )
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row is None:
        return None
    return row

    