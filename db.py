import sqlite3

conn = sqlite3.connect("saas.db", check_same_thread=False)
c = conn.cursor()

# ---------------- USERS ----------------
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    skills TEXT,
    resume TEXT
)''')

# ---------------- JOBS ----------------
c.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    email TEXT,
    title TEXT,
    description TEXT
)''')

# ---------------- AUTH (NEW - IMPORTANT) ----------------
c.execute('''CREATE TABLE IF NOT EXISTS auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)''')

conn.commit()

# ---------------- FUNCTIONS ----------------

def add_user(name, email, skills, resume=""):
    c.execute(
        "INSERT INTO users (name,email,skills,resume) VALUES (?,?,?,?)",
        (name, email, skills, resume)
    )
    conn.commit()

def add_job(company, email, title, desc):
    c.execute(
        "INSERT INTO jobs (company,email,title,description) VALUES (?,?,?,?)",
        (company, email, title, desc)
    )
    conn.commit()

def get_jobs():
    return c.execute("SELECT * FROM jobs").fetchall()

def get_users():
    return c.execute("SELECT * FROM users").fetchall()
