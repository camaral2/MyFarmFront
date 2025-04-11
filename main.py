from datetime import datetime
import requests  # Add this import at the top of your app.py
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
import calendar
import time
from api_client import APIClient
import api_client
from user_login import User_Login
from util import get_moon_phase, translate_phase_moon, month_desc
from culture import culture_blueprint
from auth import auth_blueprint
from events import events_blueprint
from datetime import timedelta

from flask_login import login_required, current_user, LoginManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

api_url = "http://127.0.0.1:8000/"  # Replace with your API URL

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app=app)

@login_manager.user_loader
def load_user(user_id):
    user_data = session.get('user_data')
    if user_data and str(user_data.get('id')) == user_id:
        return User_Login(
            id=user_data.get('id'),
            name=user_data.get('name'),
            email=user_data.get('email')
        )
    return None

@app.context_processor
def inject_user():
    return dict(current_user=current_user)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    
@app.errorhandler(401)
def custom_401(error):
    return render_template("401.html"), 401

@login_required
@app.route("/")
def admin_dashboard():
    try:
        client = APIClient(api_url)        
        cultures = client.get("/culture")
    except RuntimeError as e:
        flash(str(e), "error")
        cultures = []
    
    try:
        moon_phase_english = get_moon_phase() 
        moon_phase_portuguese = translate_phase_moon(moon_phase_english)
    except requests.exceptions.RequestException as e:
        flash(f"Moon Phase - Error: {str(e)}", "error")
        
        
    months = list(range(1, 13))
    list_month_desc = month_desc()
    current_month = datetime.now().month
    current_month_desc = list_month_desc[current_month-1]

    return render_template("index.html", 
        cultures=cultures, 
        moon_phase = moon_phase_english,
        moon_phase_portugues = moon_phase_portuguese,
        months = months,
        month_desc = list_month_desc,
        current_month_desc = current_month_desc,
        current_month = current_month
        )

app.register_blueprint(culture_blueprint, url_prefix='/culture')
app.register_blueprint(events_blueprint, url_prefix='/event')
app.register_blueprint(auth_blueprint, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)