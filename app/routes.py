from app import app, db
from app.models import *
from app.forms import *
import flask
from flask import render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, timedelta

import random
import pdb

db.create_all()

SUCC_MSG = [
    'Good job!',
    'Awesome!',
    'Correct!',
    'You rock!',
    'Great!'
]

FAIL_MSG = [
    'Not quite!',
    'Opps! Try again!',
    'Almost!',
    'Keep trying!'
]

ENC_MSG = [
    'You can do it!',
    'You\'re doing great!',
    'Keep going!'
]

@app.before_request
def before_request():
    #Makes it so that the session times out after timedelta minutes of inactivity
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    session.modified = True
    flask.g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Player.query.filter_by(name=form.player.data).first()
        if user is None:
            flash('Invalid Player')
            return redirect(url_for('login'))
        login_user(user, remember=False)
        session['streak'] = 0
        session['solved'] = 0
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        player = Player(name=form.player.data)
        player.settings = {
            'add': 'true',
            'sub': 'false',
            'mul': 'false',
            'max': '10',
            'neg': 'false',
            'retry': 'true'
        }
        db.session.add(player)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def generate_problem():
    player = Player.query.filter_by(id=current_user.id).first()
    settings = player.settings

    max_num = int(settings['max'])
    min_num = int(settings['min'])

    top = random.randint(min_num, max_num)

    if settings['neg'] == 'true':
        bottom = random.randint(min_num, max_num)
    else:
        bottom = random.randint(min_num, top)

    opers = []
    if settings['add'] == 'true':
        opers.append('+') 
    if settings['sub'] == 'true':
        opers.append('-') 
    if settings['mul'] == 'true':
        opers.append('x') 
    oper = random.choice(opers)

    retval = {
        'top': top,
        'bottom': bottom,
        'oper': oper
    }

    return retval

@app.route('/new_problem', methods=['POST'])
@login_required
def new_problem():
    
    retval = generate_problem()
    
    return jsonify(retval)

@app.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    param_fail = False
    top = int(request.values.get('top'))
    bottom = int(request.values.get('bottom'))
    oper = request.values.get('oper')
    
    # breakpoint()
    try:
        answer = int(request.values.get('answer'))
    except:
        param_fail = True

    retval = {}
    player = Player.query.filter_by(id=current_user.id).first()

    if param_fail:
        retval['success'] = False
        retval['msg'] = 'Oops, try again!'
        if player.settings.get('retry') == 'true':
            retval['bottom'] = bottom
            retval['top'] = top
            retval['oper'] = oper
        else:
            next_prob = generate_problem()
            retval = {**retval, **next_prob}

    else:
        if oper == '+':
            if top + bottom == answer:
                retval['success'] = True
                retval['alert_msg'] = random.choice(SUCC_MSG)
            else:
                retval['success'] = False
                retval['alert_msg'] = random.choice(FAIL_MSG)

        elif oper == '-':
            if top - bottom == answer:
                retval['success'] = True
                retval['alert_msg'] = random.choice(SUCC_MSG)
            else:
                retval['success'] = False
                retval['alert_msg'] = random.choice(FAIL_MSG)

        elif oper == 'x':
            if top * bottom == answer:
                retval['success'] = True
                retval['alert_msg'] = random.choice(SUCC_MSG)
            else:
                retval['success'] = False
                retval['alert_msg'] = random.choice(FAIL_MSG)

        retval['enc_msg'] = random.choice(ENC_MSG)

        if not retval['success'] and player.settings.get('retry') == 'true':
            next_prob = {
                'top': top,
                'bottom': bottom,
                'oper': oper
            }
        else:
            next_prob = generate_problem()

        if not retval['success']:
            session['streak'] = 0
        else:
            session['solved'] += 1
            session['streak'] += 1
        retval['solved'] = session['solved']
        retval['streak'] = session['streak']

        if session['streak'] > player.streak:
            player.streak = session['streak']
            retval['high_streak'] = session['streak']
            db.session.commit()
        retval = {**retval, **next_prob}

    return jsonify(retval)

@app.route('/get_settings', methods=['POST'])
@login_required
def get_settings():
    player = Player.query.filter_by(id=current_user.id).first()
    settings = player.settings
    # pdb.set_trace()
    if len(settings) <= 0:
        return jsonify('')
    else:
        return jsonify(settings)

@app.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    player = Player.query.filter_by(id=current_user.id).first()

    settings = {}
    settings['add'] = request.values.get('add')
    settings['sub'] = request.values.get('sub')
    settings['mul'] = request.values.get('mul')
    settings['max'] = request.values.get('max')
    settings['min'] = request.values.get('min')
    settings['neg'] = request.values.get('neg')
    settings['retry'] = request.values.get('retry')

    try:
        int(settings['max'])
    except:
        return jsonify({'msg':'invalid max_number'})

    try:
        int(settings['min'])
    except:
        return jsonify({'msg':'invalid min_number'})

    player.settings = settings

    db.session.commit()
    
    return jsonify({'msg':'success'}), 200

@app.route('/get_high_streak', methods=['POST'])
@login_required
def get_high_streak():
    player = Player.query.filter_by(id=current_user.id).first()
    if player.streak is None:
        player.streak = 0
    retval = {}
    retval['high_streak'] = player.streak

    db.session.commit()

    return jsonify(retval)
