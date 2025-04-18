import sqlite3
import hashlib
from flask import g 



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('Facts.db')
    return g.db


def addUser( mail, name, password):
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS userdata (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email VARCHAR(255) NOT NULL,
                       username VARCHAR(255) NOT NULL,
                       password VARCHAR(255) NOT NULL
    )
                       ''')
    conn.commit()
    
    cur = conn.execute('SELECT email from userdata')
    for _mail in cur:
        if(_mail[0] == mail): return False
    
    password = hashlib.sha256(password).hexdigest()
    conn.execute('''
    INSERT INTO userdata ( email, username, password)
    VALUES ( ?, ?, ?)
    ''', ( mail, name, password))
    conn.commit()

    print("DATA STORED")
    return True

def get_user_id(_mail, _password):
    _password = _password.encode()
    _password = hashlib.sha256(_password).hexdigest()

    conn = get_db()
    cur = conn.execute('''SELECT id FROM userdata
                        WHERE email = ? AND password = ?
                       ''',(_mail, _password))
    row = cur.fetchone()
    if row is not None:
        user_id = row[0] 
    else:
        user_id = None

    print('printing CUR')
    print(user_id)
    return user_id


def loginCheck(mail, password):
    password = password.encode()
    password = hashlib.sha256(password).hexdigest()

    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS userdata (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email VARCHAR(255) NOT NULL,
                       username VARCHAR(255) NOT NULL,
                       password VARCHAR(255) NOT NULL
    )
                       ''')
    conn.commit()
    cur = conn.execute('SELECT email, password from userdata')
    for row in cur:
        if row is not None:
            if row[0]==mail and row[1]==password : return True
    return False

def mailCheck(mail):
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS userdata (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email VARCHAR(255) NOT NULL,
                       username VARCHAR(255) NOT NULL,
                       password VARCHAR(255) NOT NULL
    )
                       ''')
    conn.commit()
    cur = conn.execute('SELECT email from userdata')
    for row in cur:
        if row[0]==mail : return True
    return False



from app import app1


@app1.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()