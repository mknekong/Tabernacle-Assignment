from datetime import datetime

import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc

from .models import Content
from . import db

views = Blueprint('views',__name__)
id = uuid.uuid1()

@views.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    data = Content.query.order_by(desc(Content.created_date)).all()
    if request.method == 'POST':
        search = request.form['search']
        data = Content.query.filter(Content.heading.like("%"+search+"%")).all()
    return render_template('dashboard.html',data=data)

@views.route('/create',methods=['GET','POST'])
@login_required
def create():

    if request.method == 'POST':
        heading = request.form['heading']
        description = request.form['description']
        user = current_user.email
        name = current_user.name
        event = Content(event=id.hex,email=user,name=name,heading=heading,description=description,created_date=datetime.now())
        db.session.add(event)
        db.session.commit()
        flash('Event Recorded Successfully!')
    return render_template('create.html')

@views.route('/view',methods=['GET','POST'])
@login_required
def view():
    data = Content.query.filter_by(email=current_user.email).order_by(desc(Content.id)).all()
    return render_template('view.html',data=data)

@views.route('/modal/<int:event_id>',methods=['POST'])
@login_required
def modal(event_id):
    data = Content.query.filter_by(id=event_id).all()
    for d in data:
        db.session.delete(d)
    db.session.commit()
    if request.method == 'POST':
        email = current_user.email
        name = current_user.name
        heading = request.form['heading1']
        description = request.form['description1']
        created_date = datetime.now()
        event = Content(event=id.hex,email=email,name=name,heading=heading,description=description,created_date=created_date)
        db.session.add(event)
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('views.view'))
    return f'Emplooyee id does not exist'

@views.route('/delete/<int:data_id>',methods=['POST'])
@login_required
def delete(data_id):
    data = Content.query.filter_by(id=data_id).first()
    db.session.delete(data)
    db.session.commit()
    flash('Event deleted!')
    return redirect(url_for('views.view'))