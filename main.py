from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Mock data
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "Admin"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "User"},
]

@app.route("/")
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template("index.html", users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Add your authentication logic here (e.g., check against database)
        if email == "admin@example.com" and password == "admin123":
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')  # Mensagem de erro
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/add-culture', methods=['GET', 'POST'])
def add_culture():
    if request.method == 'POST':
        name = request.form.get('name')
        month = request.form.get('month')
        is_active = True if request.form.get('isActive') else False
        
        # Validation
        if not name:
            flash('Name is mandatory!', 'error')
        else:
            # Save to database (pseudo-code)
            # db.save(name, month, is_active)
            flash('User added successfully!', 'success')
            return redirect(url_for('add_culture'))  # PRG pattern
            
    return render_template('add_culture.html')

if __name__ == "__main__":
    app.run(debug=True)