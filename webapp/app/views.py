import os
import re
from flask import (
    render_template, flash, redirect, request, Flask, url_for,
    make_response, session, send_file)

from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user)

from app import app, db, models

from .models import Account, Recordings

from schedpack import my_timer
from datetime import datetime


from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Account.query.filter(Account.id == int(user_id)).first()

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/home', methods=('GET', 'POST'))
@login_required
def home():

    recordings = Recordings.query.filter(Recordings.user_id == current_user.id).all()

    return render_template('record/index.html', recordings = recordings)


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        elif Account.query.filter_by(user=username).first() is not None:
            error = f'User {username} is already  registered.'

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            newuser = Account(
                user=username,
                # hash the password so cannot be accessed by anyone else
                password=generate_password_hash(password)
                )
            
            db.session.add(newuser)
            db.session.commit()

            flash("Account created successfully")

            return redirect(url_for('login'))

        flash(error)
    return render_template('auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = Account.query.filter_by(user=username).first()

        if user:  # if user exists
            # checks password with database
            if (check_password_hash(user.password, password)):
                login_user(user)  # logs in
                flash("Logged in successfully")
                return redirect(url_for('home'))
            else:
                flash("Incorrect Password")
                logging.warning('User entered the wrong password')
                return redirect(url_for('login'))
        else:
            flash("User does not exist")
            return redirect('/login')
        

        if user is None:
            error = 'Incorrect username.'

        flash(error)

    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logged out successfully")
    return redirect('/login')


@app.route('/record', methods=('GET','POST'))
@login_required
def record():
    if request.method == 'POST':
        
        instream = request.form.get('station')


        start_time = request.form.get('start_time')
        time_arr = re.split('[-:]',start_time)

        year    = int(time_arr[0])
        month   = int(time_arr[1])
        day     = int(time_arr[2])
        hour    = int(time_arr[3])
        minutes = int(time_arr[4])
        seconds = int(time_arr[5])

        file_name = request.form.get('file_name')
        duration  = request.form.get('duration')


        my_timer.runtest(datetime(year,month,day,hour,minutes,seconds),duration,instream, file_name)

        error = None

        if not file_name:
            error = 'File name is required.'

        if not duration:
            error = 'Recording duration is required.'

        if error is not None:
            flash(error)
        else:

            newrecording = Recordings(
                user_id=current_user.id,
                name=file_name,
                track_length = duration
                )
            
            db.session.add(newrecording)
            db.session.commit()
            return redirect(url_for('home'))
 
    return render_template('record/record.html')


@app.route('/download/<filename>')#, methods=('POST',))
def download(filename):
    flash(f'{filename}.mp3')
    return send_file(f'/home/ben/Documents/Dev/RadioRecorder - master/webapp/files/{filename}.mp3')
