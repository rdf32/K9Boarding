from operator import and_
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask.globals import session
from .models import User, Pet, Appointment
from werkzeug.security import generate_password_hash, check_password_hash
# use . to import from __init__
from . import admin_required, db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    events = []
    # join of two tables
    for p, a in db.session.query(Pet, Appointment).filter(Pet.id == Appointment.pet_id).all():
        events.append({
            "name": str(p.name),
            "date": str(a.date),
            "app_id": a.id,
            "pet_id": str(p.id)
        })
        
    return render_template("admin.html", user=current_user, events=events)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone_num = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('Email must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, phone=phone_num, password=generate_password_hash(password1, method='sha256'))
            # commit user to database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # maps to the home function in views
            return redirect(url_for('views.home'))
            
    return render_template("sign_up.html", user=current_user)

@auth.route('/admin-board', methods=['GET', 'POST'])
@login_required
@admin_required
def board():
    if request.method == 'POST':
        email = request.form.get('email')
        p_name = request.form.get('pname')
        type = str((request.form['type']))
        date = request.form.get('date')

        user = User.query.filter_by(email=email).first()

        appointments = []
        for row in (Appointment.query.filter_by(date=date).all()):
            appointments.append(row)
        # need to add more robust logic to all of this to make sure no errors occur (i know some can right now)
        if len(appointments) < 15:
            if user:
                # might change this to pet_id and have to query the user info first to get the pets' ids'
                pet = Pet.query.filter_by(user_id=(user.id), name=p_name).first()
                if pet:
                # add user to database
                    new_appt = Appointment(type=type, date=date, pet_id=(pet.id))
                    # commit user to database
                    db.session.add(new_appt)
                    db.session.commit()
                    flash('Appointment created!', category='success')
                    # maps to the home function in views
                    return redirect(url_for('auth.admin'))
                else: 
                    flash('Pet not found', category='error')
            else: 
                flash('Owner not found', category='error')
        else:
            flash('Limit of 15 animals reached', category='error')

    return render_template("boarding.html", user=current_user)

@auth.route('/admin-addUser', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('Email must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            # commit user to database
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            # maps to the home function in views
            return redirect(url_for('auth.admin'))
            
    return render_template("sign_up.html", user=current_user)

@auth.route('/admin-addPet', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_pet():
    if request.method == 'POST':
        email = request.form.get('email')
        p_name = request.form.get('pname')
        user = User.query.filter_by(email=email).first()

        if user:
           # add user to database
            new_pet = Pet(name=p_name, user_id = user.id)
            # commit user to database
            db.session.add(new_pet)
            db.session.commit()
            flash('Pet added!', category='success')
            # maps to the home function in views
            return redirect(url_for('auth.admin'))
        else:
            flash("User does not exist", category="error")
            
            
    return render_template("pet_add.html", user=current_user)

@auth.route('/admin-search', methods=['GET', 'POST'])
@login_required
@admin_required
def search_user():
    if request.method == 'POST':
        pet = request.form.get('pSearch')
        name = request.form.get('oSearch')
        # write logic to deal with only searching with first name
        if name:
            names = [x for x in name.split(" ")]
            if len(names) == 2:

                first_name, last_name = names[0], names[1]

                users = []
                for u, p in db.session.query(User,Pet).filter(and_(and_(User.first_name.like(first_name), User.last_name.like(last_name)), User.id == Pet.user_id)).all():
                    users.append({
                        'owner_email': str(u.email),
                        'first_name': str(u.first_name),
                        'last_name': str(u.last_name),
                        'phone' : str(u.phone),
                        'pet_name': str(p.name),
                        'pet_id': str(p.id)

                    })
                if users:
                    return render_template("search.html", user=current_user, users=users)
                else:
                    flash("User not found", category="error")
            else:
                flash("Must provide first and last name", category='error')
        if pet:
            pets = []
            for u, p in db.session.query(User,Pet).filter(and_(User.id == Pet.user_id, Pet.name.like(pet))).all():
                pets.append({
                    'owner_email': str(u.email),
                    'first_name': str(u.first_name),
                    'last_name': str(u.last_name),
                    'phone' : str(u.phone),
                    'pet_name': str(p.name),
                    'pet_id': str(p.id)

                })
            if pets:
                return render_template("search.html", user=current_user, pets=pets)
            else:
                flash("Pet not found", category="error")
    return render_template("search.html", user=current_user)


