import sqlite3
from config import ADMIN_ID

async def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            is_active INTEGER DEFAULT 1,
            used_start_promo INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

async def add_user(user_id: int, username: str, first_name: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    ''', (user_id, username, first_name))
    conn.commit()
    conn.close()

async def get_user(user_id: int):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

async def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

async def set_user_active_status(user_id: int, status: bool):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_active = ? WHERE user_id = ?', (status, user_id))
    conn.commit()
    conn.close()

async def get_stat():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    users_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
    active_users_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 0')
    no_active_users_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE used_start_promo = 1')
    count_users_start_promotion = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "users_count": users_count,
        "active_users_count": active_users_count,
        "no_active_users_count": no_active_users_count,
        "count_users_start_promotion": count_users_start_promotion
    } 