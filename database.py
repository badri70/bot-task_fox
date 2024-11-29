import sqlite3
from datetime import datetime


def connect_to_db(db_name="task_manager.db"):
    conn = sqlite3.connect(db_name)
    return conn


def create_all_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        telegram_id INTEGER UNIQUE NOT NULL,
        created_at TEXT DEFAULT (DATETIME('now')),
        settings TEXT DEFAULT '{}',
        last_login TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER,
        created_at TEXT DEFAULT (DATETIME('now')),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        category_id INTEGER,
        priority TEXT,
        deadline TEXT,
        status TEXT DEFAULT 'в процессе',
        created_at TEXT DEFAULT (DATETIME('now')),
        updated_at TEXT DEFAULT (DATETIME('now')),
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
        FOREIGN KEY (priority_id) REFERENCES priorities (id) ON DELETE SET NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        reminder_time TEXT NOT NULL,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("Все таблицы успешно созданы!")


def add_category(name, user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO categories (name, user_id) 
        VALUES (?, ?);
        """, (name, user_id))
        conn.commit()
        print(f"Категория '{name}' успешно добавлена.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении категории: {e}")
    finally:
        conn.close()


def get_categories(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, name, created_at 
    FROM categories
    WHERE user_id = ?;
    """, (user_id,))
    categories = cursor.fetchall()
    conn.close()

    # Преобразуем данные в читаемый формат
    return [
        {"id": row[0], "name": row[1], "created_at": row[2]}
        for row in categories
    ]


def add_task(title, description, user_id, category_id=None, priority=None, deadline=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO tasks (title, description, user_id, category_id, priority_id, deadline)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (title, description, user_id, category_id, priority, deadline))
        conn.commit()
        print(f"Задача '{title}' успешно добавлена.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка при добавлении задачи: {e}")
    finally:
        conn.close()


def get_tasks(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        t.id, 
        t.title, 
        t.description, 
        c.name AS category_name, 
        t.priority_id, 
        t.deadline, 
        t.status, 
        t.created_at
    FROM tasks t
    LEFT JOIN categories c ON t.category_id = c.id
    WHERE t.user_id = ?;
    """, (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "category_name": row[3],  # Название категории
            "priority_id": row[4],   # ID приоритета
            "deadline": row[5],
            "status": row[6],
            "created_at": row[7]
        }
        for row in tasks
    ]


def add_user(username, telegram_id, email=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (username, email, telegram_id) 
        VALUES (?, ?, ?);
        """, (username, email, telegram_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Пользователь с таким Telegram ID уже существует.")
    finally:
        conn.close()


def user_exists(telegram_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id FROM users WHERE telegram_id = ?;
    """, (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def update_user_settings(telegram_id, settings):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users
    SET settings = ?, last_login = DATETIME('now')
    WHERE telegram_id = ?;
    """, (settings, telegram_id))
    conn.commit()
    conn.close()