import sqlite3

conn = sqlite3.connect("saas.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    skills TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    company TEXT,
    email TEXT,
    title TEXT,
    description TEXT
)''')

conn.commit()

def add_user(name, email, skills):
    c.execute("INSERT INTO users (name,email,skills) VALUES (?,?,?)",
              (name,email,skills))
    conn.commit()

def add_job(company, email, title, desc):
    c.execute("INSERT INTO jobs (company,email,title,description) VALUES (?,?,?,?)",
              (company,email,title,desc))
    conn.commit()

def get_jobs():
    return c.execute("SELECT * FROM jobs").fetchall()
