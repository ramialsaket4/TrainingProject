import os
from functools import wraps
from flask import Flask, jsonify, session, redirect, url_for, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, '../frontend/templates'),
    static_folder=os.path.join(BASE_DIR, '../frontend/static')
)

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super-secret-key-change-this')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized, please log in'}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return jsonify({"status": "healthy", "service": "expense_backend"})

@app.route('/health')
def health():
    return jsonify({"status": "UP"})


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email') or (request.json.get('email') if request.is_json else None)
    password = request.form.get('password') or (request.json.get('password') if request.is_json else None)

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, password FROM users WHERE email = %s;", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        
        if request.form:
            return redirect(url_for('dashboard'))
        return jsonify({'message': 'Login successful'}), 200
    
    return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name') or (request.json.get('name') if request.is_json else None)
    email = request.form.get('email') or (request.json.get('email') if request.is_json else None)
    password = request.form.get('password') or (request.json.get('password') if request.is_json else None)

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    hashed_pw = generate_password_hash(password, method='scrypt')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
            (name, email, hashed_pw)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        if request.form:
            return redirect(url_for('login_page'))
        return jsonify({'message': 'User registered successfully', 'id': user_id}), 201
    except Exception:
        conn.rollback()
        return jsonify({'error': 'Registration failed. Email may already exist.'}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/categories')
@login_required
def categories_page():
    return render_template('categories.html')

@app.route('/add-expense')
@login_required
def add_expense_page():
    return render_template('expense_form.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
