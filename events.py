from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from api_client import APIClient
from utils.util import get_mode_desc, list_modes

from datetime import datetime, timedelta
from utils.config import setting

events_blueprint = Blueprint('events', __name__)

api_url = setting.api_url # Replace with your API URL


@events_blueprint.route('/<int:idculture>/<int:id>', methods=['GET', 'POST'])
def edit_event(idculture, id):
    
    client = APIClient(api_url)

    is_edit = False
    modes = list_modes()

    if request.method == 'GET':    
        if id > 0: 
            event_culture = client.get("event_culture/item/" + str(id))
            
            print('Teste - event_culture: ' + str(event_culture))    
            
            
            if event_culture:
                culture =event_culture["culture"]
                is_edit = True
                return render_template('event/edit_event.html', 
                                       culture = culture, is_edit = is_edit, 
                                       modes = modes, 
                                       event_culture = event_culture,
                                       datetime=datetime)
    

        culture = client.get("culture/" + str(idculture))

    
    if request.method == 'POST':
        id: int | 0 = request.form.get('id')
        idculture: int | 0 = request.form.get('idculture')
        
        date_str: str | None = request.form.get('date_event')
        event: str | None = request.form.get('event')
        mode: int | 0 = request.form.get('mode')
        detail: str | None = request.form.get('detail')
        
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_iso = date_obj.isoformat()
        
        culture = {
            "event": event,
            "mode": mode,
            "detail": detail,
            "culture_id": idculture,
            "date": date_iso
        }
                
        try:
            if int(id) > 0:                
                event = client.put("event_culture/" + str(id), json=culture)
                flash('Event updated successfully!', 'success')
            else:
                event = client.post("event_culture", json=culture)            
                flash('Event added successfully!', 'success')
                
            return redirect(url_for('events.list_events', idculture = idculture))
        except RuntimeError as e:
            flash(str(e), "error")

    
    
    return render_template('event/edit_event.html', 
                           culture = culture, 
                           is_edit = is_edit, 
                           modes = modes,
                           datetime=datetime)


@events_blueprint.route("/<int:idculture>", methods=['GET', 'POST'])
def list_events(idculture):
    
    client = APIClient(api_url)

    # Cultura selecionada via POST (ex: <select>)
    if request.method == 'POST':
        selected = request.form.get('culture')
        if selected and selected.isdigit():
            idculture = int(selected)
    
    # Busca todas as culturas para o <select>
    cultures = client.get("culture")
    
    # Lógica para determinar qual cultura exibir
    if not idculture:
        idculture = session.get('idculture')
            
    if not idculture and cultures:
        idculture = cultures[0]['id']
    
    culture = client.get("culture/" + str(idculture))
    events_culture = client.get("event_culture/" + str(idculture))
    
    for event in events_culture:
        if isinstance(event["date"], str):
            event["date"] = datetime.fromisoformat(event["date"])
            
        event['mode_desc'] = get_mode_desc(event['mode'])
         
    #save de last culture show
    session['idculture'] = idculture
    
    return render_template("event/list_event.html", 
                           events_culture=events_culture,
                           idculture = idculture,
                           culture = culture, 
                           cultures = cultures)
    
@events_blueprint.route("/<int:id>/delete", methods=["POST"])
def delete_event(id):

    try:
        client = APIClient(api_url)
        client.delete(f"event_culture/{id}")
    
        flash("Event deleted successfully", "success")
    except RuntimeError as e:
        flash(str(e), "error")
            
    return redirect(url_for("events.list_events", idculture=session.get("idculture")))
