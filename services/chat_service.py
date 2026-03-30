from services.db_service import (
    create_chat,
    save_message,
    load_messages,
    get_user_chats
)

def start_new_chat(user_id):
    return create_chat(user_id, "New Chat")


def add_user_message(chat_id, message):
    save_message(chat_id, "user", message)


def add_ai_message(chat_id, message):
    save_message(chat_id, "assistant", message)


def fetch_messages(chat_id):
    return load_messages(chat_id)


def fetch_user_chats(user_id):
    return get_user_chats(user_id)

def update_chat_title(chat_id, title):
    from services.db_service import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE chats SET title=%s WHERE id=%s"
    cursor.execute(query, (title, chat_id))

    conn.commit()
    cursor.close()
    conn.close()
