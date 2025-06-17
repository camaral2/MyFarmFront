from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import requests
from flask_login import login_user, login_required, logout_user

from user_login import User_Login

from utils.config import setting


auth_blueprint = Blueprint('auth', __name__)

api_url = setting.api_url  # Replace with your API URL

@auth_blueprint.route('/login', methods=['GET', 'POST'])
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
                        
            user_data = api_data.get('user')
            user = User_Login(
                id=user_data.get('id'),
                name=user_data.get('name'),
                email=user_data.get('email')
            )
            
            login_user(user = user, remember=True)

            session['user_data'] = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }            
            session['user_token'] = api_data.get('access_token')  # Store API token if provided
                                    
            return redirect(url_for('admin_dashboard'))
                        
        except requests.exceptions.RequestException as e:
            error_msg = "Invalid credentials" if response.status_code == requests.codes.forbidden else f"API Error: {str(e)}"
            flash(error_msg, "error")

    return render_template('login.html')

@login_required
@auth_blueprint.route('/logout')
def logout():
    logout_user()
    session.clear()
        
    return redirect(url_for('auth.login'))
