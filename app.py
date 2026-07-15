from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )
    ''')

    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            image TEXT,
            description TEXT,
            category TEXT
        )
    ''')

    # Sample products (only if empty)
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO products (name, price, image, description, category) VALUES ('Face Wash', 200, 'p1.webp', 'Skin care product', 'beauty')")
        cursor.execute("INSERT INTO products (name, price, image, description, category) VALUES ('Cream', 300, 'p2.webp', 'Moisturizer', 'beauty')")
        cursor.execute("INSERT INTO products (name, price, image, description, category) VALUES ('Serum', 500, 'p3.webp', 'Glow serum', 'beauty')")

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('test.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            return render_template('success.html')
        else:
            return "<h3 style='color:red;'>Invalid Email or Password</h3>"

    return render_template('login.html')


# ---------------- BEAUTY PRODUCTS ----------------
@app.route('/beauty')
def beauty():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE category='beauty'")
    products = cursor.fetchall()

    conn.close()

    return render_template('beauty.html', products=products)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)