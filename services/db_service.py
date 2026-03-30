import mysql.connector
import os

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



