from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session

app = Flask(__name__)

# Secret key for sessions and flash messages
app.secret_key = "supersecretkey"

# Configure session type
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# In-memory user store (you can later replace with database)
users = {}

# ========================
# Home Page
# ========================
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username, logged_in=True)
    return render_template('index.html', logged_in=False)

# ========================
# Login Page
# ========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

# ========================
# Signup Page
# ========================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            flash("Username already exists. Please choose another one.", "error")
            return redirect(url_for('signup'))

        # Save user details
        users[username] = {'email': email, 'password': password}
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# ========================
# Logout
# ========================
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('index'))

# ========================
# Run Server
# ========================
if __name__ == '__main__':
    app.run(debug=True)
