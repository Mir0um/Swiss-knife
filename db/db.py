import sqlite3
import hashlib
import os

def create_database():
    conn = sqlite3.connect('db/sesion.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reset_token TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_table_as_dict(db_name='sesion.db', table_name='users'):
    conn = sqlite3.connect("db/" + db_name)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return result

def add_user(username, password, role='user', db_name='sesion.db'):
    hashpw = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("db/" + db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashpw, role))
    conn.commit()
    conn.close()

def delete_user(username, db_name='sesion.db'):
    conn = sqlite3.connect("db/" + db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def verify_user(username, password, db_name='sesion.db'):
    hashpw = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("db/" + db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT username, role FROM users WHERE username = ? AND password = ?', (username, hashpw))
    user = cursor.fetchone() 
    conn.close()
    return user if user else None

if os.path.exists('db/sesion.db') == False:
    create_database()
    add_user('admin', 'password' , role="admin")  # Remplacez par des identifiants sécurisés
    add_user('toto', 'ddsf16SDFSD5', role="user de test")  # Remplacez par des identifiants sécurisés
    add_user('Чиполлино', 'пароль' , role="Още летa, пяло на ти попле за мони Ева,...")  # Remplacez par des identifiants sécurisés