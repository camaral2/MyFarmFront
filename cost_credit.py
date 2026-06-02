from flask import Blueprint, flash, redirect, render_template, request, url_for
from api_client import APIClient
from utils.config import setting
from datetime import datetime

cost_credit_blueprint = Blueprint('cost_credit', __name__, template_folder='templates/cost_credit')

api_url = setting.api_url

@cost_credit_blueprint.route('/', methods=['GET'])
def list_cost_credits():
    try:
        client = APIClient(api_url)
        
        # Get filters from request
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        culture_id = request.args.get('culture_id')
        
        # Fetch cultures for filter
        cultures = client.get("/culture")
        
        # Fetch cost_credits
        # Construct query parameters if API supports them, otherwise filter in python
        # Assuming API might not support complex filtering yet, but let's try to pass them if possible or filter client side
        # For now, let's get all and filter client side as per common pattern if API is simple, 
        # but ideally we should pass params. The prompt didn't specify API filtering capabilities details, 
        # so I will fetch all and filter in Python for safety unless I see API docs.
        # However, looking at the user request "a listagem ter o filtro por período e cultura", 
        # it implies the UI needs it.
        
        cost_credits = client.get("/cost_credit")
        if cost_credits is None:
            cost_credits = []

        filtered_list = []
        total_cost = 0
        total_credit = 0
        
        for item in cost_credits:
            # Apply filters
            item_date = item.get('date')
            item_culture_id = item.get('culture_id')
            
            if start_date and item_date < start_date:
                continue
            if end_date and item_date > end_date:
                continue
            if culture_id and culture_id != '0' and str(item_culture_id) != str(culture_id):
                continue
                
            filtered_list.append(item)
            
            # Calculate totals
            amount = item.get('amount', 0)
            if item.get('type') == 'Cost':
                total_cost += amount
            elif item.get('type') == 'Credit':
                total_credit += amount

        # Enrich with culture name
        culture_map = {c['id']: c['name'] for c in cultures} if cultures else {}
        for item in filtered_list:
            item['culture_name'] = culture_map.get(item.get('culture_id'), 'Unknown')

    except RuntimeError as e:
        flash(str(e), "error")
        cultures = []
        filtered_list = []
        total_cost = 0
        total_credit = 0

    return render_template("cost_credit/list.html", 
                           cost_credits=filtered_list, 
                           cultures=cultures,
                           total_cost=total_cost,
                           total_credit=total_credit,
                           filters={'start_date': start_date, 'end_date': end_date, 'culture_id': culture_id})

@cost_credit_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_cost_credit(id):
    client = APIClient(api_url)
    
    if request.method == 'POST':
        try:
            data = {
                "type": request.form.get('type'),
                "amount": float(request.form.get('amount')),
                "description": request.form.get('description'),
                "date": request.form.get('date'),
                "culture_id": int(request.form.get('culture_id'))
            }
            
            if id == 0:
                client.post("/cost_credit", json=data)
                flash('Entry added successfully!', 'success')
            else:
                client.put(f"/cost_credit/{id}", json=data)
                flash('Entry updated successfully!', 'success')
                
            return redirect(url_for('cost_credit.list_cost_credits'))
            
        except RuntimeError as e:
            flash(str(e), "error")
        except ValueError as e:
             flash(f"Invalid input: {str(e)}", "error")

    # GET request
    entry = None
    if id > 0:
        try:
            entry = client.get(f"/cost_credit/{id}")
        except RuntimeError as e:
            flash(str(e), "error")
            
    try:
        cultures = client.get("/culture")
    except RuntimeError:
        cultures = []

    return render_template('cost_credit/form.html', entry=entry, cultures=cultures, id=id)

@cost_credit_blueprint.route('/delete/<int:id>')
def delete_cost_credit(id):
    try:
        client = APIClient(api_url)
        client.delete(f"/cost_credit/{id}")
        flash('Entry deleted successfully!', 'success')
    except RuntimeError as e:
        flash(str(e), "error")
        
    return redirect(url_for('cost_credit.list_cost_credits'))
