from flask import Blueprint, render_template, request, redirect, url_for
from dataclasses import dataclass
import backend_data

@dataclass
class Session:
    username: str | None = None
    password: str | None = None
    engine: object | None = None

@dataclass
class Cache:
    content: str | None = ''

session = Session()
cache = Cache()

riffrank = Blueprint('riffrank', __name__)

@riffrank.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        action = request.form.get('action')

        if action == 'signup':
            backend_data.run(action, None, username, password)
            return redirect(url_for('riffrank.login'))
        
        engine = backend_data.run(action, None, username, password)

        if engine == -2:
            return render_template('login_error.html')

        session.username = username
        session.password = password
        session.engine = engine

        return redirect(url_for('riffrank.artists'))

    return render_template('login.html')

@riffrank.route('/artists', methods = ['POST', 'GET'])
def artists():
    if request.method == 'POST':
        artist_id = request.form.get('artist_id')
        cache.content = artist_id
        return redirect(url_for('riffrank.artist'))
    
    artists = backend_data.run(['list_artists'], session.engine)

    return render_template('artists.html', artists = artists)

@riffrank.route('/artist', methods = ['POST', 'GET'])
def artist():
    if request.method == 'POST':
        if 'album_id' in request.form.keys():
            album_id = request.form.get('album_id')
            cache.content = album_id
            return redirect(url_for('riffrank.album'))

        score = int(request.form.get('score'))
        tier = int(request.form.get('tier'))
        favorite = request.form.get('favorite') == 'on'

        artist_id = cache.content        
        backend_data.run(['rate_artist', artist_id, session.username, score, tier, favorite], session.engine)

    artist_id = cache.content
    artist, albums = backend_data.run(['list_artist', artist_id], session.engine)

    rating = backend_data.run(['get_artist_rating', artist_id, session.username], session.engine)

    return render_template('artist.html', artist = artist, albums = albums, rating = rating)

@riffrank.route('/album', methods = ['POST', 'GET'])
def album():
    if request.method == 'POST':
        if 'artist_id' in request.form.keys():
            artist_id = request.form.get('artist_id')
            cache.content = artist_id
            return redirect(url_for('riffrank.artist'))

        elif 'track_id' in request.form.keys():
            score = int(request.form.get('score'))
            melody = int(request.form.get('melody'))
            solo = int(request.form.get('solo'))
            vocals = int(request.form.get('vocals'))
            tier = int(request.form.get('tier'))
            favorite = request.form.get('favorite') == 'on'

            track_id = request.form.get('track_id')
            backend_data.run(
                [
                    'rate_track',
                    track_id,
                    session.username,
                    score,
                    {'melody': melody, 'solo': solo, 'vocals': vocals},
                    tier,
                    favorite
                ],
                session.engine
            )

        else:
            score = int(request.form.get('score'))
            tier = int(request.form.get('tier'))
            favorite = request.form.get('favorite') == 'on'

            album_id = cache.content
            backend_data.run(['rate_album', album_id, session.username, score, tier, favorite], session.engine)

    album_id = cache.content
    album, tracks = backend_data.run(['list_album', album_id], session.engine)
    artist = backend_data.run(['list_artist', album[0]], session.engine)[0]

    rating = backend_data.run(['get_album_rating', album_id, session.username], session.engine)
    track_ratings = {track[1]: backend_data.run(['get_track_rating', track[1], session.username], session.engine) for track in tracks}

    return render_template('album.html', artist = artist, album = album, tracks = tracks, rating = rating, track_ratings = track_ratings)
