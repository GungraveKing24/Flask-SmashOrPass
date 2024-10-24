from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db, oauth
from app.models import users, pokemon
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os, secrets, string

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

@app.route('/login/google')
def login_google():
    nonce = os.urandom(16).hex()
    session['nonce'] = nonce
    redirect_uri = url_for('auth_callback_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/callback/google')
def auth_callback_google():
    if 'error' in request.args:
        error_message = request.args.get('error')
        flash(f"Error de autenticación: {error_message}", "error")
        return redirect(url_for('login'))

    try:
        token = oauth.google.authorize_access_token()  # Obtener el token de acceso
        
        # Cambia esta línea para obtener la información del usuario
        user_info = oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()  

        print("User Info:", user_info)  # Imprimir la información del usuario para depuración

        # Verifica si el nombre está disponible
        if 'name' not in user_info:
            flash("No se pudo obtener el nombre del usuario.", "error")
            return redirect(url_for('login'))

        # Resto del código para manejar el usuario...
        user = users.query.filter_by(email=user_info['email']).first()

        if not user:
            random_password = generate_random_password()
            new_user = users(name=user_info['name'], email=user_info['email'], password=random_password)  # Usa una contraseña aleatoria
            db.session.add(new_user)
            db.session.commit()
            user = new_user

        # Guardar en la sesión
        session['user_id'] = user.id
        session['user_name'] = user.name
        return redirect(url_for('index'))

    except Exception as e:
        flash("Ocurrió un error al procesar el inicio de sesión", "error")
        return redirect(url_for('login'))

def generate_random_password(length=12):
    """Genera una contraseña aleatoria de una longitud especificada."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

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
            flash('Registro desactivado permanentemente')
            #hashed_password = generate_password_hash(password)
            #new_user = users(name=name, email=email, password=hashed_password)
            #db.session.add(new_user)
            #db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))