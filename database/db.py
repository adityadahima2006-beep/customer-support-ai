import sqlite3

DB_NAME = "database/chat_history.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================
# Create Database Table
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# Save Chat
# ==========================================

def save_chat(username, user_message, bot_response):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (
            username,
            user_message,
            bot_response
        )
        VALUES (?, ?, ?)
        """,
        (
            username,
            user_message,
            bot_response
        )
    )

    conn.commit()
    conn.close()


# ==========================================
# Get Chat History
# ==========================================

def get_chat_history(username=None):

    conn = get_connection()
    cursor = conn.cursor()

    if username:

        cursor.execute(
            """
            SELECT
                user_message,
                bot_response,
                timestamp
            FROM chat_history
            WHERE username = ?
            ORDER BY id DESC
            """,
            (username,)
        )

    else:

        cursor.execute(
            """
            SELECT
                username,
                user_message,
                bot_response,
                timestamp
            FROM chat_history
            ORDER BY id DESC
            """
        )

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================================
# Total Users
# ==========================================

def get_total_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(DISTINCT username) FROM chat_history"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# Total Chats
# ==========================================

def get_total_chats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM chat_history"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# Sentiment Counts
# ==========================================

def get_sentiment_counts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT bot_response FROM chat_history"
    )

    rows = cursor.fetchall()

    positive = 0
    neutral = 0
    negative = 0

    for row in rows:

        text = row[0]

        if "😊" in text:
            positive += 1

        elif "😔" in text:
            negative += 1

        else:
            neutral += 1

    conn.close()

    return positive, neutral, negative


# ==========================================
# Recent Chats
# ==========================================

def get_recent_chats(limit=10):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            username,
            user_message,
            bot_response,
            timestamp
        FROM chat_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    chats = cursor.fetchall()

    conn.close()

    return chats


# ==========================================
# Search Chats
# ==========================================

def search_chats(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            username,
            user_message,
            bot_response,
            timestamp
        FROM chat_history
        WHERE
            username LIKE ?
            OR user_message LIKE ?
            OR bot_response LIKE ?
        ORDER BY id DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    chats = cursor.fetchall()

    conn.close()

    return chats





# ==========================================
# Export All Chats
# ==========================================

def get_all_chats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            username,
            user_message,
            bot_response,
            timestamp
        FROM chat_history
        ORDER BY id DESC
    """)

    chats = cursor.fetchall()

    conn.close()

    return chats