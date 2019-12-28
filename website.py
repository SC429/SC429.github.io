from flask import Flask, render_template, request, session    #need to download flask
from flask_session import Session    #need to download FLASK-SESSION
import os
from sqlalchemy import create_engine  #need to download sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

engine = create_engine('postgres://ehqnnhaxklfutw:28e7fb579f4bfc92d4039dcd34e693c689b57b211ea60b78240e3018f30c6940@ec2-174-129-33-30.compute-1.amazonaws.com:5432/dab40c5k7lkmt8')
db = engine.connect()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/thankyou', methods=["POST"])
def thankyou():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    db.execute("INSERT INTO contact_info (fname, lname, email) VALUES (%s, %s, %s)", (fname, lname, email))
    return render_template('complete.html', fname = fname)

@app.route('/data', methods=["POST"])
def data():
    code = request.form.get("password-admin")
    if code == "1234":
        data = db.execute("SELECT fname, lname, email FROM contact_info").fetchall()
        for entry in data:
            print(f"{entry.fname} {entry.lname} {entry.email}")  #prints onto command prompt
    return index()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
