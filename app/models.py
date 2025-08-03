from .db import get_db

def get_all_users():
    cursor = get_db().cursor()
    cursor.execute("SELECT id, name, email FROM users")
    return cursor.fetchall()

def get_user_by_id(user_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def create_user(name, email, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    db.commit()
    return cursor.lastrowid

def update_user(user_id, name, email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    db.commit()

def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()

def search_users_by_name(name):
    cursor = get_db().cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
    return cursor.fetchall()

def verify_login(email, password):
    cursor = get_db().cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
    return cursor.fetchone()