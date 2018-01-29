from flask import Flask, redirect, request, abort
from twilio.twiml.messaging_response import MessagingResponse

from spotify import Client
from spotify.auth.scope import Scope
from spotify.auth.user import authorize_url, User


app = Flask(__name__)

spotify = None
PLAYLIST_ID = 'PUT_PLAYLIST_ID_HERE'


@app.route('/init')
def init():
    permissions = [v for k, v in Scope.__dict__.items() if '__' not in k]
    return redirect(authorize_url(scopes=permissions), 302)


@app.route('/authorize')
def authorize():
    global spotify
    code = request.values.get('code', None)
    spotify = Client(User(code))
    return 'OK'


@app.route('/enqueue', methods=['GET', 'POST'])
def enqueue():
    body = request.values.get('Body')
    track = search(body)
    if not track:
        abort(400)

    me = spotify.v1.me.fetch()
    playlist = spotify.v1.users.get(me.id).playlists.get(PLAYLIST_ID).fetch()
    playlist.tracks.add([track.uri])

    artists = [artist.name for artist in track.artists]

    mr = MessagingResponse()
    mr.message(body='Added {} by {} to the playlist!'.format(track.name, ' & '.join(artists)))
    return mr.to_xml()


def search(body):
    result = spotify.v1.search.get(body, ['track'])
    for track in result.tracks:
        return track

    return None


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
