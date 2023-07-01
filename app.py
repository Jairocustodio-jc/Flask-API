from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        pokemon_data = get_pokemon_data(pokemon_name)
        if pokemon_data:
            return render_template('pokemon.html', pokemon_data=pokemon_data)
        else:
            return render_template('error.html')
    return render_template('index.html')

def get_pokemon_data(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_data = {
            'name': data['name'].capitalize(),
            'type': get_pokemon_type(data),
            'images': get_pokemon_images(data),
            'moves': get_pokemon_moves(data)
        }
        return pokemon_data
    return None

def get_pokemon_type(data):
    types = []
    if 'types' in data:
        for type_data in data['types']:
            types.append(type_data['type']['name'].capitalize())
    return types

def get_pokemon_images(data):
    images = []
    if 'sprites' in data:
        sprites = data['sprites']
        images.append(sprites['front_default'])
        images.append(sprites['front_shiny'])
        images.append(sprites['back_default'])
        images.append(sprites['back_shiny'])
    return images

def get_pokemon_moves(data):
    moves = []
    if 'moves' in data:
        for move_data in data['moves']:
            moves.append(move_data['move']['name'])
    return moves

if __name__ == '__main__':
    app.run()
