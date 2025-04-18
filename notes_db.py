import sqlite3, datetime
from app import session, app1
from database import get_db
from flask import g

date_time = datetime.date.today()
# Convert datetime object to string
datetime_str = date_time.strftime('%Y-%m-%d')

#This function will add notes to db
def add_note(note1):
    conn = get_db()
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS usernotes (
                 n_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 note_date TEXT,
                 notes TEXT,
                 user_id INTEGER,
                 FOREIGN KEY (user_id) REFERENCES userdata(id)
                 )
                 ''')
    conn.commit()

    #NEED TO MODIFY AS YOU HAVE MADE A SEPERATE FUNCTION
    cur = conn.execute('''
        SELECT n_id FROM usernotes
        WHERE user_id = ? AND note_date = ?
    ''', (session['userId'], datetime_str))
    
    row = cur.fetchone()
    new_value = note1
    if row is not None:
        #first we need to retrive the existig value and concatinate with new one
        cur = conn.execute(f"SELECT notes FROM usernotes WHERE note_date = {datetime_str} AND user_id = {session['userId']}")
        for row in cur:
            new_value = row[0] + new_value
            break

        #here we will update the column as per todays date
        conn.execute(f'''
                    UPDATE usernotes SET notes = ? WHERE note_date = ? AND user_id = ?
                    ''', (new_value, datetime_str, session['userId']))
        conn.commit()   

    #If that 'if'condition didn't works means we have to create a new row
    else: 
        cur =  conn.execute("INSERT INTO usernotes (note_date, notes, user_id) VALUES (?, ?, ?)", (datetime_str, new_value, session['userId']))
        conn.commit()

def get_note(date):
    conn = get_db()

    conn.execute('''
                 CREATE TABLE IF NOT EXISTS usernotes (
                 n_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 note_date TEXT,
                 notes TEXT,
                 user_id INTEGER,
                 FOREIGN KEY (user_id) REFERENCES userdata(id))
                 ''')
    conn.commit()

    cur = conn.execute('''
        SELECT notes FROM usernotes
        WHERE user_id = ? AND note_date = ?
    ''', (session['userId'], date))
    
    row = cur.fetchone()
    if row is not None:
        return row[0]
    return ''

