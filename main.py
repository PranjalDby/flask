from flask import Flask, render_template,request,session,url_for,redirect
from werkzeug.security import generate_password_hash,check_password_hash
import os
import dotenv
app = Flask(__name__)
app.secret_key = os.getenv(key='SECRET_KEY')

# example User

USER = {
    'username':"admin",
    'password':generate_password_hash('password123')
}
@app.route('/')
def hello_main():
    return render_template('static.html')


@app.route('/login',methods = ["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USER['username'] and check_password_hash(USER['password'],password):
            session['user'] = username
            return redirect(url_for('dashboard'))
            
        else:
            error = 'Invalid Credentials'
            return render_template('error.html')
            
            
    return render_template('loginpage.html',error = error)


@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html',user=session['user'])
    
@app.route('/about')
def aboutMe():
    return render_template('aboutMe.html')




if __name__ == '__main__':
    app.run(debug=True)