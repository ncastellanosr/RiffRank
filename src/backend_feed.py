from flask import Blueprint, render_template, request, redirect, url_for
from dataclasses import dataclass
import backend_data

class Session:
    def __init__(self):
        self.is_open = False
    def open(self, username, password, engine):
        self.username = username
        self.password = password
        self.engine = engine
        self.is_open = True

@dataclass
class Cache:
    content: str | None = ''

session = Session()
cache = Cache()

riffrank = Blueprint('riffrank', __name__)

@riffrank.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        engine = backend_data.run('login', None, None, username, password)

        if engine == -2:
            return redirect(url_for('riffrank.login', error='invalid_credentials'))

        session.open(username, password, engine)

        return redirect(url_for('riffrank.artists'))
    
    error_dict = {
        None: '',
        'invalid_credentials': 'Invalid Credentials!'
    }

    error = request.args.get('error')

    return render_template('login.html', error = error_dict[error])

@riffrank.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            return redirect(url_for('riffrank.signup', error='password_match'))

        response = backend_data.run('signup', None, email, username, password)

        if response == -3:
            return redirect(url_for('riffrank.signup', error='user_exists'))
        elif response == -4:
            return redirect(url_for('riffrank.signup', error='busy_name'))

        return redirect(url_for('riffrank.login'))

    error_dict = {
        None: '',
        'password_match': 'Passwords do not match!',
        'user_exists': 'An user is already linked with this email address!',
        'busy_name': 'This username is already being used!'
    }

    error = request.args.get('error')

    return render_template('signup.html', error = error_dict[error])

def common_header():
    if not session.is_open:
        return redirect(url_for('riffrank.login'))

    if request.method == "POST":
        if 'profile-page' in request.form.keys():
            return redirect(url_for('riffrank.profile'))

        if 'search' in request.form.keys():
            search_string = request.form.get('search_string')
            cache.content = [
                search_string,
                backend_data.run(['search_artists', search_string], session.engine),
                backend_data.run(['search_albums', search_string], session.engine),
                backend_data.run(['search_tracks', search_string], session.engine)
            ]

            return redirect(url_for('riffrank.search'))
    
    return None

@riffrank.route('/', methods = ['POST', 'GET'])
def main_page():
    result = common_header()
    if result: return result

    return render_template('index.html')

@riffrank.route('/profile', methods = ['POST', 'GET'])
def profile():
    result = common_header()
    if result: return result

    if request.method == 'POST':
        if 'save-changes' in request.form.keys():
            new_username = request.form.get('username')
            bio = request.form.get('profile-bio')

            if new_username == session.username: new_username = None
            if bio == cache.content: bio = None

            backend_data.run(['update_user', session.username, new_username, bio], session.engine)

            if new_username is not None: session.username = new_username

    bio = backend_data.run(['get_user', session.username], session.engine)
    cache.content = bio

    return render_template('profile.html', username = session.username, bio = bio)

@riffrank.route('/search', methods = ['POST', 'GET'])
def search():
    result = common_header()
    if result: return result

    if request.method == 'POST':        
        if 'album_id' in request.form.keys():
            album_id = request.form.get('album_id')
            cache.content = album_id
            return redirect(url_for('riffrank.album'))

        if 'artist_id' in request.form.keys():
            artist_id = request.form.get('artist_id')
            cache.content = artist_id
            return redirect(url_for('riffrank.artist'))
    
    results = cache.content

    return render_template('search_results.html', search_string = results[0], artists = results[1], albums = results[2], tracks = results[3])

@riffrank.route('/artists', methods = ['POST', 'GET'])
def artists():
    result = common_header()
    if result: return result

    if request.method == 'POST':
        artist_id = request.form.get('artist_id')
        cache.content = artist_id

        return redirect(url_for('riffrank.artist'))
    
    artists = backend_data.run(['list_artists'], session.engine)

    return render_template('artists.html', artists = artists)

@riffrank.route('/artist', methods = ['POST', 'GET'])
def artist():
    result = common_header()
    if result: return result

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
    result = common_header()
    if result: return result

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
