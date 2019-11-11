import os
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, session, render_template, request, redirect

app = Flask(__name__)

engine = create_engine('sqlite:///forum.db', convert_unicode=True)
s = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

#s = Session()

from models import *

Base.metadata.create_all(engine)

#@app.teardown_request
#def remove_session(ex=None):
    #session.remove()

@app.route('/')
def home():
    return "idk"

@app.route('/user/<user>')
def user(user):
    # Hämtar variabeln current_user från databasen genom att kolla efter ett specifikt användar-id i "users"
    current_user = s.query(User).filter_by(userId=user).first()
    
    # Om användaren inte existerar
    if current_user is None:
        return "No user with that name exists!"

    return render_template("Forum/user.html", row=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        # Spara användarens id i sessionsvariabeln user.
        # En sessionsvariabel är en variabel som sparas för en klient/webbläsare så länge man är inne på vilken sida som helst från den här webbservern.
        
        user = s.query(User).filter_by(name=request.form.get('username')).first()

        if not user.check_password(request.form.get('password')):
            print('Error, wrong password')
            return render_template('Forum/login.html')
        
        session['user'] = str(user.userId)

        return redirect("/user/" + session['user'])

    return render_template('Forum/login.html')

# Vilken tråd som klienten/webbläsaren försöker komma åt
@app.route('/threads/<thread>', methods=['GET', 'POST'])
def threads(thread):
    if request.method == 'POST':
        #current_user = s.query(User).filter_by(userId=session['user']).first()
        print(request.form.get('comment'), session['user'])

        # Skapar ett nytt kommentarsobjekt
        comment = Comment(session['user'], thread, request.form.get('comment'))
        s.add(comment)
        
        # Lägger till objektet i databasen
        s.commit()

    # Hämtar variabeln currentThread från databasen genom att kolla efter ett specifikt tråd-id i "threads"
    currentThread = s.query(Thread).filter_by(threadId=thread).first()

    comments = s.query(Comment).filter_by(threadId=thread).all()

    return render_template("Forum/thread.html", thread=currentThread, comments=comments)

# Lista med trådar på det här forumet
@app.route('/list')
def list():
    rows = s.query(Thread).all()
    return render_template("Forum/forum.html", rows=rows)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if s.query(s.query(User).filter_by(name=request.form.get('username')).exists()).scalar():
            return render_template('Forum/register.html')
        else:
            user = User(request.form.get('username'), request.form.get('password'))
            s.add(user)

            # Lägger till objektet i databasen
            s.commit()

            session['user'] = str(user.userId)
            return redirect("/user/" + session['user'])

    return render_template('Forum/register.html')

# Om man startade programmet genom den här filen så körs detta
if __name__ == '__main__':
    app.secret_key = os.urandom(52)
    app.run(debug=True)