from flask import Flask, render_template, Response, request, url_for, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import json, os, requests


# Obtén la ruta absoluta para la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy()
db.init_app(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable=False)

class pokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pokemon = db.Column(db.String, unique = True, nullable = False)
    nivel = db.Column(db.Integer, nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/home')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    pokemon_id = request.cookies.get('pokemon_id')

    if not pokemon_id:
        pokemon_id = 1
        
    pokemon_id = int(pokemon_id)

    return render_template('smashpass.html', pokemon_id=pokemon_id)

@app.route('/get_pokemon/<int:pokemon_id>')
def get_pokemon(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        session['pokemon_id'] = pokemon_id
        pokemon_data = response.json()
        image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
        name = pokemon_data['name']
        return jsonify({"name": name, "image_url": image_url})
    return jsonify({"error": "Pokémon not found"}), 404

@app.route('/savepokemon/<string:pokemon_name>/<int:pokemon_level>', methods=['POST'])
def savepokemon(pokemon_name, pokemon_level):
    if 'user_id' in session:
        # Verifica si ya existe un Pokémon con el mismo nombre
        existing_pokemon = pokemon.query.filter_by(pokemon=pokemon_name).first()
        if existing_pokemon:
            return jsonify({"status": "error", "message": "This Pokémon already exists."}), 400

        new_pokemon = pokemon(pokemon=pokemon_name, nivel=pokemon_level, id_user=session['user_id'])
        db.session.add(new_pokemon)
        db.session.commit()
        return jsonify({"status": "success", "message": "Pokémon saved!"}), 200

    return jsonify({"status": "error", "message": "User not logged in"}), 403

@app.route('/get_pokemon_id')
def get_pokemon_id():
    pokemon_id = session.get('pokemon_id', 1)
    return jsonify({"pokemon_id": pokemon_id})
    

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
    return redirect(url_for('login'))

def pokemons():
    url = 'https://pokeapi.co/api/v2/pokemon'
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)