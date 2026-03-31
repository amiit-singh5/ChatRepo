import mysql.connector
import os
import bcrypt

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user


def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed)
    )
    conn.commit()

    cursor.close()
    conn.close()


import bcrypt

def verify_user(username, password):
    user = get_user(username)

    if not user:
        return None

    stored_password = user["password"]

    # 🔥 convert DB value to bytes (IMPORTANT)
    if isinstance(stored_password, str):
        stored_password = stored_password.encode()

    if bcrypt.checkpw(password.encode(), stored_password):
        return user["id"]

    return None

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ai_chat"
        # user="root",
        # unix_socket="/var/run/mysqld/mysqld.sock",
        # database="ai_chat"
        # host="localhost",
        # user="root",
        # password=os.getenv("MYSQL_PASSWORD"),
        # database="ai_chat"
    )

def save_message(chat_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO messages (chat_id, role, content)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (chat_id, role, content))

    conn.commit()
    cursor.close()
    conn.close()

def load_messages(chat_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT role, content FROM messages WHERE chat_id=%s ORDER BY id ASC"
    cursor.execute(query, (chat_id,))

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def create_chat(user_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO chats (user_id, title) VALUES (%s, %s)"
    cursor.execute(query, (user_id, title))

    conn.commit()
    chat_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return chat_id

def get_user_chats(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
            SELECT id, title 
            FROM chats 
            WHERE user_id=%s AND archived=FALSE
    """
    cursor.execute(query, (user_id,))

    chats = cursor.fetchall()

    cursor.close()
    conn.close()

    return chats

def delete_chat(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE chat_id=%s", (chat_id,))
    cursor.execute("DELETE FROM chats WHERE id=%s", (chat_id,))

    conn.commit()
    cursor.close()
    conn.close()

def archive_chat(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE chats SET archived=TRUE WHERE id=%s",
        (chat_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

def get_archived_chats(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT id, title 
    FROM chats 
    WHERE user_id=%s AND archived=TRUE
    """

    cursor.execute(query, (user_id,))
    chats = cursor.fetchall()

    cursor.close()
    conn.close()

    return chats

def restore_chat(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE chats SET archived=FALSE WHERE id=%s",
        (chat_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

# def get_user_id(username):
#     conn = get_connection()
#     cursor = conn.cursor()

#     query = "SELECT id FROM users WHERE username=%s"
#     cursor.execute(query, (username,))
#     result = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     return result[0] if result else None

def get_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()

    # check user
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
    else:
        # create new user
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        conn.commit()
        user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return user_id



