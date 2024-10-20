from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import users, pokemon
import requests

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/smash_pass')
def smash_pass():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('smashpass.html')

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    if request.method == 'POST':
        fetch = requests.get(url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = users.query.filter_by(name=name, password=password).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))