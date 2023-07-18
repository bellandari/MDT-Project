from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Ped
from . import db
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

file_path = os.path.abspath(os.getcwd())+"instance/mdt.db"

engine = create_engine('sqlite:///'+file_path)
Session = sessionmaker(bind=engine)
session = Session()

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
        
    return render_template("home.html", user=current_user)

@views.route('/disclaimer', methods=['GET', 'POST'])
def disclaimer():
        
    return render_template("disclaimer.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():     
    
    first = request.form.get('firstName')
    last = request.form.get('lastName')
    dob = request.form.get('dob')                
    
    results = session.query(Ped).filter(Ped.lastName==last, Ped.firstName==first, Ped.dob==dob)
        
    return render_template("search.html", user=current_user, results = results, show_modal=True)

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