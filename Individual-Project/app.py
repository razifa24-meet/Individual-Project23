from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {"apiKey": "AIzaSyA_XD8ALr38QWr4_S-Zwyjwyu0nr-nHaLw",
  "authDomain": "csminigame-fe8f4.firebaseapp.com",
  "databaseURL": "https://csminigame-fe8f4-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "csminigame-fe8f4",
  "storageBucket": "csminigame-fe8f4.appspot.com",
  "messagingSenderId": "690106197114",
  "appId": "1:690106197114:web:ed1cc05a8145996d7707c3", 
  "databaseURL": "https://csminigame-fe8f4-default-rtdb.europe-west1.firebasedatabase.app/" }



firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            print("HELLO, WORKED")
            return redirect(url_for('frive'))
        except Exception as e:
            error = "Authentication failed"
            print(e)
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        bio = request.form['bio']
        full_name = request.form['fullname']
        
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": full_name, "email": email, "username" : username, "bio" : bio}
            db.child("Users").child(UID).update(user)
            return redirect(url_for('frive'))

        except:
            error = "Authentication failed"

    return render_template("signup.html")



@app.route('/signout')
def signout():
    auth.current_user = None
    login_session['user'] = None
    return redirect(url_for(''))

@app.route('/frive', methods=['GET', 'POST'])
def frive():

    return render_template("frive.html")




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)