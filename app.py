"""
Department of Computer Science & Engineering — Backend Server
"""

import os
import re

import pymysql
import pymysql.cursors
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Enable CORS for all routes (Cross-Origin issue fix karne ke liye)
CORS(app, supports_credentials=True)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-this-in-production")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),  # XAMPP default is blank
    "database": os.environ.get("DB_NAME", "cs_department"),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def get_db():
    """Open a fresh database connection."""
    try:
        return pymysql.connect(**DB_CONFIG)
    except pymysql.MySQLError as e:
        print(f"Database Connection Error: {e}")
        return None


# --------------------------------------------------------------------------
# Frontend
# --------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------------------------------
# API: Register
# --------------------------------------------------------------------------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    roll_no = (data.get("roll_no") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name:
        return jsonify(error="Please enter your name."), 400
    if not roll_no:
        return jsonify(error="Please enter your roll number."), 400
    if not EMAIL_RE.match(email):
        return jsonify(error="Enter a valid email address."), 400
    if len(password) < 6:
        return jsonify(error="Password must be at least 6 characters."), 400

    db = get_db()
    if not db:
        return jsonify(error="Database connection failed. Ensure MySQL/XAMPP is running."), 500

    try:
        with db.cursor() as cur:
            cur.execute("SELECT id FROM students WHERE email = %s", (email,))
            if cur.fetchone():
                return jsonify(error="An account with this email already exists."), 409

            cur.execute("SELECT id FROM students WHERE roll_no = %s", (roll_no,))
            if cur.fetchone():
                return jsonify(error="This roll number is already registered."), 409

            password_hash = generate_password_hash(password)
            cur.execute(
                "INSERT INTO students (full_name, roll_no, email, password_hash) "
                "VALUES (%s, %s, %s, %s)",
                (name, roll_no, email, password_hash),
            )
    except pymysql.MySQLError as err:
        return jsonify(error=f"Database error: {str(err)}"), 500
    finally:
        db.close()

    session["user_email"] = email
    return jsonify(ok=True, name=name, roll_no=roll_no, email=email)


# --------------------------------------------------------------------------
# API: Login
# --------------------------------------------------------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    db = get_db()
    if not db:
        return jsonify(error="Database connection failed."), 500

    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT full_name, roll_no, email, password_hash FROM students WHERE email = %s",
                (email,),
            )
            user = cur.fetchone()
    finally:
        db.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify(error="Invalid email or password."), 401

    session["user_email"] = user["email"]
    return jsonify(ok=True, name=user["full_name"], roll_no=user["roll_no"], email=user["email"])


# --------------------------------------------------------------------------
# API: Logout
# --------------------------------------------------------------------------
@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify(ok=True)


# --------------------------------------------------------------------------
# API: Current Session
# --------------------------------------------------------------------------
@app.route("/api/me")
def me():
    email = session.get("user_email")
    if not email:
        return jsonify(loggedIn=False)

    db = get_db()
    if not db:
        return jsonify(loggedIn=False)

    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT full_name, roll_no, email FROM students WHERE email = %s", (email,)
            )
            user = cur.fetchone()
    finally:
        db.close()

    if not user:
        session.clear()
        return jsonify(loggedIn=False)

    return jsonify(loggedIn=True, name=user["full_name"], roll_no=user["roll_no"], email=user["email"])


# --------------------------------------------------------------------------
# API: Public Department Content
# --------------------------------------------------------------------------
@app.route("/api/faculty")
def api_faculty():
    db = get_db()
    if not db:
        return jsonify(faculty=[])
    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT name, designation, qualification, email "
                "FROM faculty ORDER BY sort_order ASC, name ASC"
            )
            rows = cur.fetchall()
    finally:
        db.close()
    return jsonify(faculty=rows)


@app.route("/api/notifications")
def api_notifications():
    db = get_db()
    if not db:
        return jsonify(notifications=[])
    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT title, body, DATE_FORMAT(posted_on, '%Y-%m-%d') AS posted_on, "
                "is_important FROM notifications ORDER BY posted_on DESC"
            )
            rows = cur.fetchall()
    finally:
        db.close()
    for r in rows:
        r["is_important"] = bool(r["is_important"])
    return jsonify(notifications=rows)


@app.route("/api/events")
def api_events():
    db = get_db()
    if not db:
        return jsonify(events=[])
    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT title, description, DATE_FORMAT(event_date, '%Y-%m-%d') AS event_date, "
                "location, category FROM events ORDER BY event_date ASC"
            )
            rows = cur.fetchall()
    finally:
        db.close()
    return jsonify(events=rows)


@app.route("/api/activities")
def api_activities():
    db = get_db()
    if not db:
        return jsonify(activities=[])
    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT title, description, DATE_FORMAT(activity_date, '%Y-%m-%d') AS activity_date, "
                "category FROM activities ORDER BY activity_date DESC"
            )
            rows = cur.fetchall()
    finally:
        db.close()
    return jsonify(activities=rows)


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)