from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Ped
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
        
    return render_template("home.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():     
    
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    dob = request.form.get('dob')
    
    results = Ped.query.filter(firstName==firstName).filter(lastName==lastName).filter(dob==dob).limit(1).first()
    
    print(results)
        
    return render_template("search.html", user=current_user, results = results)

@views.route('/help', methods=['GET', 'POST'])
@login_required
def help():
        
    return render_template("help.html", user=current_user)

@views.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    
    if request.method == 'POST':
        
        note = request.form.get('note')
        
        if len(note) < 1:
            
            flash('Note is too short.', category='error')
        
        else:
            
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            
            flash('Note added!', category='success')
        
    return render_template("reports.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})