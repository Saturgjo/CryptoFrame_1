from flask import Flask, render_template, request, redirect, url_for, send_file, session
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'nqm159kkk'  # Change this to a strong secret key

# Dummy user for demonstration purposes
users = {
    'test_user': generate_password_hash('test_password')
}

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password matches
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again!"
    return render_template('login.html')

# Route for the dashboard (only accessible if logged in)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Route for downloading a file
@app.route('/download')
def download():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Make sure the file to download exists
    
    filepath = 'static/example_file.txt'
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found!"

# Route to logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Make sure you create a 'static/example_file.txt' before running this
    app.run(debug=True)