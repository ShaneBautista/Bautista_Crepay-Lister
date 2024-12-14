import mysql.connector
from mysql.connector import Error
import hashlib
import bcrypt

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'crepay_lister',
}

def db_connect():
    """Establish a database connection."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as err:
        print(f"Database Error: {err}")
        return None

def register_user(username, password):
    """Register a new user."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return "Username already exists."
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cursor.close()
            conn.close()
            return "Registration successful."
    except Error as err:
        return f"Database Error: {err}"

def login_user(username, password):
    """Check if user exists and return user data."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
    except Error as err:
        print(f"Database Error: {err}")
        return None

def add_payment_reminder(user_id, name, email, account,amount, payment_date):
    """Add a payment reminder."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO payment_reminders (user_id, name, email, credit_account,amount, next_payment_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, name, email, account,amount, payment_date))
            conn.commit()
            cursor.close()
            conn.close()
            return "Payment reminder added successfully."
    except Error as err:
        return f"Database Error: {err}"

def fetch_reminders(user_id):
    """Fetch payment reminders for a user."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor()
            query = """
            SELECT name, email, credit_account, amount, next_payment_date
            FROM payment_reminders
            WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            reminders = cursor.fetchall()
            cursor.close()
            conn.close()
            return reminders
    except Error as err:
        print(f"Database Error: {err}")
        return None

def fetch_upcoming_reminders():
    """Fetch upcoming payment reminders."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor(dictionary=True)  # Ensure we fetch results as dictionaries
            query = """
            SELECT name, email, credit_account, amount, next_payment_date
            FROM payment_reminders
            WHERE next_payment_date >= CURDATE()  -- This ensures only upcoming reminders are fetched
            ORDER BY next_payment_date
            """
            cursor.execute(query)
            reminders = cursor.fetchall()
            cursor.close()
            conn.close()

            if reminders:
                return reminders
            else:
                print("No upcoming reminders found.")
                return []
    except Error as err:
        print(f"Database Error: {err}")
        return None
    
    
def authenticate_worker(username, password):
    """Authenticate worker based on username and password."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM workers WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))  # Beware of SQL injection in real apps
            worker = cursor.fetchone()
            cursor.close()
            conn.close()
            return worker
    except Error as err:
        print(f"Database Error: {err}")
        return None

def fetch_upcoming_reminders():
    """Fetch upcoming payment reminders."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT name, email, credit_account, amount, next_payment_date
            FROM payment_reminders
            WHERE next_payment_date >= CURDATE()  -- This ensures only upcoming reminders are fetched
            ORDER BY next_payment_date
            """
            cursor.execute(query)
            reminders = cursor.fetchall()
            cursor.close()
            conn.close()
            return reminders
    except Error as err:
        print(f"Database Error: {err}")
        return None

def register_worker(username, password, email):
    """Register a new worker in the database."""
    try:
        conn = db_connect()
        if conn:
            cursor = conn.cursor()

            # Insert the worker's details into the 'workers' table
            cursor.execute("""
                INSERT INTO workers (username, password, email) 
                VALUES (%s, %s, %s)
            """, (username, password, email))

            conn.commit()
            cursor.close()
            conn.close()

            return True  # Indicate that the registration was successful
    except Error as err:
        print(f"Database Error: {err}")
        return False  # Indicate that the registration failed