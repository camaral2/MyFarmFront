import calendar
from flask import Blueprint, flash, redirect, render_template, request, url_for
from api_client import APIClient

culture_blueprint = Blueprint('culture', __name__, template_folder='templates/culture')

api_url = "http://127.0.0.1:8000/"  # Replace with your API URL

@culture_blueprint.route('/')
def list_cultures():
    try:
        client = APIClient(api_url)
        
        cultures = client.get("/culture")
        
        for culture in cultures:
            culture["month_start_name"] = calendar.month_name[culture["month_start"]] if culture.get("month_start") else ''
            culture["month_end_name"] = calendar.month_name[culture["month_end"]] if culture.get("month_end") else ''
    
    except RuntimeError as e:
        flash(str(e), "error")
        cultures = []
    
    return render_template("culture/list_culture.html", cultures=cultures)

@culture_blueprint.route('/<int:id>', methods=['GET', 'POST'])
def edit_culture(id):
    
    if request.method == 'POST':

        is_edit = True
        
        id: int | 0 = request.form.get('id')
        
        name: str | None = request.form.get('name')
        month_start: int | 0 = request.form.get('month_start')
        month_end: int | 0 = request.form.get('month_end')
        is_active: bool = True if request.form.get('isActive') else False
        
        culture = {
            "name": name,
            "month_start": month_start,
            "month_end": month_end,
            "is_active": str(is_active)
        }
                
        client = APIClient(api_url)
                
        try:
            if id:                
                cultures = client.put("culture/" + str(id), json=culture)
                flash('User updated successfully!', 'success')
            else:
                cultures = client.post("culture", json=culture)            
                flash('User added successfully!', 'success')
            
            return redirect(url_for('culture.list_cultures'))
        except RuntimeError as e:
            flash(str(e), "error")
    else:
        culture = None
        is_edit = False
        
        if id:
            try:
                client = APIClient(api_url)
                culture = client.get("/culture/" + str(id))
                is_edit = True
                
                culture["month_start_name"] = calendar.month_name[culture["month_start"]] if culture.get("month_start") else ''
                culture["month_end_name"] = calendar.month_name[culture["month_end"]] if culture.get("month_end") else ''
    

            except RuntimeError as e:
                flash(str(e), "error")
                
        
    months = list(enumerate(['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'], 1))
    
    return render_template('culture/edit_culture.html', culture = culture, is_edit = is_edit, months = months)

