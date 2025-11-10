import sqlite3
import os

class Database:
    def __init__(self, db_path='data/chatbot.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT
            )
        ''')

        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT
            )
        ''')

        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # FAQs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT
            )
        ''')

        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sentiment REAL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def populate_sample_data(self):
        """Populate the database with sample data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Sample users
        users = [
            ('John Doe', 'john@example.com', '123-456-7890'),
            ('Jane Smith', 'jane@example.com', '098-765-4321'),
        ]
        cursor.executemany('INSERT OR IGNORE INTO users (name, email, phone) VALUES (?, ?, ?)', users)

        # Sample products
        products = [
            ('Laptop', 'High-performance laptop', 999.99, 'Electronics'),
            ('Headphones', 'Noise-cancelling headphones', 199.99, 'Electronics'),
            ('Book', 'Bestseller novel', 19.99, 'Books'),
        ]
        cursor.executemany('INSERT OR IGNORE INTO products (name, description, price, category) VALUES (?, ?, ?, ?)', products)

        # Sample orders
        orders = [
            (1, 1, 1, '2023-10-01', 'shipped'),
            (2, 2, 2, '2023-10-02', 'pending'),
        ]
        cursor.executemany('INSERT OR IGNORE INTO orders (user_id, product_id, quantity, order_date, status) VALUES (?, ?, ?, ?, ?)', orders)

        # Sample FAQs
        faqs = [
            ('How do I track my order?', 'You can track your order using the order number provided in your confirmation email.', 'orders'),
            ('What is your return policy?', 'We accept returns within 30 days of purchase for a full refund.', 'returns'),
            ('How do I reset my password?', 'Click on "Forgot Password" on the login page and follow the instructions.', 'account'),
        ]
        cursor.executemany('INSERT OR IGNORE INTO faqs (question, answer, category) VALUES (?, ?, ?)', faqs)

        conn.commit()
        conn.close()

    def get_user_by_email(self, email):
        """Get user by email."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_order_by_id(self, order_id):
        """Get order by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT orders.*, users.name, products.name
            FROM orders
            JOIN users ON orders.user_id = users.id
            JOIN products ON orders.product_id = products.id
            WHERE orders.id = ?
        ''', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return order

    def get_faqs_by_category(self, category=None):
        """Get FAQs, optionally filtered by category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT question, answer FROM faqs WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT question, answer FROM faqs')
        faqs = cursor.fetchall()
        conn.close()
        return faqs

    def save_conversation(self, user_id, message, response, sentiment=None):
        """Save a conversation entry."""
        import datetime
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        cursor.execute('INSERT INTO conversations (user_id, message, response, timestamp, sentiment) VALUES (?, ?, ?, ?, ?)',
                       (user_id, message, response, timestamp, sentiment))
        conn.commit()
        conn.close()
