from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from app.models import users, pokemon
from werkzeug.security import generate_password_hash, check_password_hash
import requests

@app.before_request
def log_session():
    app.logger.info(f"Session Data: {session}")

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    pokemones = pokemon.query.filter_by(id_user=session['user_id']).all()
    return render_template('index.html', pokemones=pokemones)

@app.route('/smash_pass')
def smash_pass():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('smashpass.html')

@app.route('/savepokemon/<string:pokemon_name>/<int:pokemon_id>', methods=['POST'])
def savepokemon(pokemon_name, pokemon_id):
    user_id = session.get('user_id')  # Obtenemos el ID del usuario desde la sesión
    
    # Verificamos si el Pokémon ya ha sido registrado por este usuario
    existing_pokemon = pokemon.query.filter_by(pokemon=pokemon_name, id_user=user_id).first()
    if existing_pokemon:
        return jsonify({'message': f'Pokémon {pokemon_name} ya fue registrado por este usuario.'}), 400

    # Si no existe, lo creamos y lo asociamos al usuario actual
    new_pokemon = pokemon(pokemon=pokemon_name, pokemon_id=pokemon_id, id_user=user_id)
    try:
        db.session.add(new_pokemon)
        db.session.commit()
        return jsonify({'message': f'Pokémon {pokemon_name} registrado exitosamente.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al guardar Pokémon.'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.permanent = True  # Esto asegura que la sesión dure el tiempo configurado
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            user = users.query.filter_by(name=name, email=email).first()
        except Exception as e:
            flash('Ocurrió un error al intentar acceder a la base de datos.')
        
        if user:
            flash('El usuario ya existe')
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(password)
            new_user = users(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))