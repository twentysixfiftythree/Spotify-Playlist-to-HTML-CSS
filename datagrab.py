from flask import Flask, render_template, request
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config

client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.secret)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


app = Flask(__name__)

def clean_sp_link(url):
    index = url.find("?si=")
    return url[:index]

@app.route('/form', methods =["GET", "POST"])
def get_playlist():
    """Grabs playlist from Spotify from a specified link"""
    user = request.form['spotify_user']
    playlist = request.form['spotify_playlist']
    index = playlist.find("?si=")
    playlist = playlist[:index]

    if request.method == "POST":
        playlist_features_list = ["artist","album","track_name",  "track_id",]
        playlist_df = pd.DataFrame(columns = playlist_features_list)
        playlist = sp.user_playlist_tracks(user, playlist)["items"]
        artists = []
        albums = []
        tracks = []

        for i in range(0,len(playlist)):
            name_artist = (playlist[i]["track"]["album"]["artists"][0]["name"])
            name_album = playlist[i]["track"]["album"]["name"]
            name_track = playlist[i]["track"]["name"]
            artists.append(name_artist)
            tracks.append(name_track)
            albums.append(name_album)
        dict1 = {'Artist': artists, 'Album': albums, 'Tracks': tracks}
        df = pd.DataFrame(dict1)
        return render_template('form.html',  tables=[df.to_html(classes = "green_grey_table")], titles=df.columns.values, )
    return render_template('form.html')


@app.route('/')
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug= True)
