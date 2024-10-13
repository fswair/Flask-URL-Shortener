from flask import Blueprint, request, jsonify, redirect
import random
import string
from database import add_url, get_long_url

url_shortener = Blueprint('url_shortener', __name__)

def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@url_shortener.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('longUrl')
    alias = data.get('alias')

    if not long_url:
        return jsonify({'error': 'Long URL is required'}), 400

    if alias:
        if not add_url(alias, long_url):
            return jsonify({'error': 'Alias already in use'}), 400

        short_url = alias
    else:
        while True:
            short_url = generate_short_url()
            if add_url(short_url, long_url):
                break

    return jsonify({'shortUrl': f'http://localhost:5000/{short_url}'})

@url_shortener.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    
    return jsonify({'error': 'URL not found'}), 404
