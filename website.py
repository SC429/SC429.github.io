from flask import Flask, render_template, request, session    #need to download flask
from flask_session import Session    #need to download FLASK-SESSION
import os
from sqlalchemy import create_engine  #need to download sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

engine = create_engine(os.getenv("URL_FOR_DATABASE")) #can use any database by inserting the URL in the URL_FOR_DATABASE, will need to insert a database link for program to work
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    db.execute("CREATE TABLE contact_info (id SERIAL PRIMARY KEY, fname VARCHAR NOT NULL, lname VARCHAR NOT NULL, email VARCHAR NOT NULL);")
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

    db.execute("INSERT INTO contact_info (fname, lname, email) VALUES (:fname, :lname, :email)",
        {"fname": fname, "lname": lname, "email": email})
    db.commit()

    return render_template('complete.html')

if __name__ == '__main__':
    app.run(debug=True)
