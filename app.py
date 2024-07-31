from flask import Flask, redirect, request, session, url_for
import requests
import os
from helix import Credentials

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Para la seguridad de la sesión
credentials = Credentials()

# Configura tus credenciales y el scope
CLIENT_ID = credentials.client_id
CLIENT_SECRET = credentials.secret_id
REDIRECT_URI = 'http://localhost:5000/callback'  # La URI de redirección debe coincidir con la registrada en Twitch
SCOPES = 'moderator:read:followers'

# URL de autorización
AUTH_URL = (
    f'https://id.twitch.tv/oauth2/authorize'
    f'?client_id={CLIENT_ID}'
    f'&redirect_uri={REDIRECT_URI}'
    f'&response_type=code'
    f'&scope={SCOPES.replace(" ", "+")}'
)

@app.route('/')
def home():
    return 'Bienvenido a la integración con Twitch API Helix! <a href="/login">Iniciar sesión con Twitch</a>'

@app.route('/login')
def login():
    return redirect(AUTH_URL)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, params=params)
    token_info = response.json()
    access_token = token_info.get('access_token')

    if not access_token:
        return 'Error al obtener el token de acceso', 400

    # Guardar el token de acceso en la sesión
    session['access_token'] = access_token
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    access_token = session.get('access_token')

    if not access_token:
        return redirect(url_for('login'))

    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
    user_info = response.json()

    return f'Información del usuario: {user_info}'

if __name__ == '__main__':
    app.run(debug=True)
