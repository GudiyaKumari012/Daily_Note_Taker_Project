from flask import Flask, render_template, request, redirect, url_for,session
from flask_mail import Mail,Message
import datetime
from datetime import timedelta


app1 = Flask(__name__)
app1.secret_key = 'sessionKey'
app1.permanent_session_lifetime = timedelta(days=1)

from database import addUser, get_user_id, loginCheck, mailCheck
from notes_db import get_note, add_note
    

print ("db closed")

@app1.route('/',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        print('STEP01')
        email1 = request.form['email']
        password1 = request.form['password']

        if loginCheck(email1, password1):
            session.permanent = True
            session['userId'] = get_user_id(email1, password1) 
            print(session['userId'])
            return redirect(url_for('messagePage'))
        else :
            text1 = 'User not registered, please register first'
            return render_template('login.html', msg = text1)
      
    else:
        print("LOGIN")
        return render_template("login.html")

@app1.route('/signup', methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        # id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['confirm-password']

        if password != password2: return render_template("signup.html", msg='Password is not matching')

        #will check the emailid is there in db or not
        if mailCheck(email): return render_template("signup.html", msg='email Id already exists')


        password = password.encode()
        if addUser( email, name, password):
            #yha pe register hone k bad session nahi create ho rha tha 
            #so we copied code from login
            session.permanent = True
            session['userId'] = get_user_id(email, password2) 
            print(session['userId'])
            return redirect(url_for('messagePage'))
        
            # if loginCheck(email, password2):
            #     session.permanent = True
            #     session['userId'] = get_user_id(email, password2) 
            #     print(session['userId'])
            #     return redirect(url_for('messagePage'))
            # return 'something went wrong'
        else :
            return render_template("signup.html", msg='Something went wrong')
    return render_template("signup.html")

@app1.route('/yournote',methods = ['GET', 'POST'])
def messagePage():

    if request.method == 'POST':
        add_note(request.form['content'])
        print(request.form['content'])

    date_time = datetime.date.today()
    # Convert datetime object to string
    datetime_str = date_time.strftime('%Y-%m-%d')
    prev_notes = get_note(datetime_str)
    print("NOTES")
    print(prev_notes)
    return render_template('msg.html', _date = datetime.date.today(), _note = prev_notes)

@app1.route('/logout')
def logout():
    session.pop('userId',None)
    return redirect(url_for('login'))

@app1.route('/old_notes', methods = ['GET', 'POST'])
def old_notes():
    if request.method == 'POST':
      _date = request.form['note_date']
      return render_template('old_notes.html', _date = _date, _notes = get_note(_date))


if __name__=="__main__":
    app1.run(debug=True)