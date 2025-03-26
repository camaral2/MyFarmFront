import requests  # Add this import at the top of your app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import calendar
import time

from util import translate_phase_moon

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management
api_url = "http://127.0.0.1:8000/"  # Replace with your API URL


def get_moon_phase():
    timestamp = int(time.time())  # current UNIX time
    url = f"https://api.farmsense.net/v1/moonphases/?d={timestamp}"

    response = requests.get(url)
    data = response.json()

    return  data[0]["Phase"]

@app.route("/")
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    try:
        # Fetch users from API
        response = requests.get(
            url = api_url + "/culture/active",
            headers={"Authorization": f"Bearer {session.get('user_token')}"}  # If auth is needed
        )
        response.raise_for_status()  # Raise error for bad status codes (4xx/5xx)
        cultures = response.json()  # Parse JSON response
        
        for culture in cultures:
            culture["month_start_name"] = calendar.month_name[culture["month_start"]] if culture.get("month_start") else ''
            culture["month_end_name"] = calendar.month_name[culture["month_end"]] if culture.get("month_end") else ''
    
    
    except requests.exceptions.RequestException as e:
        if response.status_code == requests.codes.unauthorized:
            flash('Session expired. <a href="/login">Click here to log in again</a>.', 'error')
        else:
            flash(f"API Error: {str(e)}", "error")
        cultures = []  # Fallback empty list   
    
    moon_phase_english = get_moon_phase() 
    
    return render_template("index.html", 
        cultures=cultures, 
        moon_phase = moon_phase_english,
        moon_phase_portugues = translate_phase_moon(moon_phase_english)
        )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Fetch users from API
            response = requests.post(
                url = api_url + "/login",
                data={"username": email, "password": password},  
            )
            response.raise_for_status()  # Raise error for bad status codes (4xx/5xx)
            
            api_data = response.json()
            session['user_token'] = api_data.get('access_token')  # Store API token if provided
                        
            user = api_data.get('user')
            session['logged_in'] = user
                                    
            return redirect(url_for('admin_dashboard'))
                        
        except requests.exceptions.RequestException as e:
            error_msg = "Invalid credentials" if response.status_code == requests.codes.forbidden else f"API Error: {str(e)}"
            flash(error_msg, "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_token', None)
    
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



@app.route("/cultures")
def list_cultures():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    try:
        # Fetch users from API
        response = requests.get(
            url = api_url + "/culture",
            headers={"Authorization": f"Bearer {session.get('user_token')}"}  # If auth is needed
        )
        response.raise_for_status()  # Raise error for bad status codes (4xx/5xx)
        cultures = response.json()  # Parse JSON response
        
        for culture in cultures:
            culture["month_start_name"] = calendar.month_name[culture["month_start"]] if culture.get("month_start") else ''
            culture["month_end_name"] = calendar.month_name[culture["month_end"]] if culture.get("month_end") else ''
    
    except requests.exceptions.RequestException as e:
        if response.status_code == requests.codes.unauthorized:
            flash('Session expired. <a href="/login">Click here to log in again</a>.', 'error')
        else:
            flash(f"API Error: {str(e)}", "error")
        cultures = []  # Fallback empty list    
    
    return render_template("culture/list_culture.html", cultures=cultures)

@app.errorhandler(401)
def custom_401(error):
    return render_template('401.html'), 401


if __name__ == "__main__":
    app.run(debug=True)