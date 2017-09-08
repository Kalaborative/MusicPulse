from flask import Flask, render_template, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

clientid = "fd2fc5fe72eb4e49b76d4c746ef312a1"
clientsecret = "c00bcfcaca4b43eb86ee6cd3297d33d8"

clientcreds = SpotifyClientCredentials(clientid, clientsecret)

sp = spotipy.Spotify(client_credentials_manager=clientcreds)

def get_artist(name):
	results = sp.search(q="artist:" + name, type='artist')
	items = results['artists']['items']
	if len(items) > 0:
		return items[0]
	else:
		return None

def show_recommendations_for_artist(artist):
	allRecommendations = []
	artist_id = artist['id']
	results = sp.recommendations(seed_artists=[artist_id])
	for track in results['tracks']:
		allRecommendations.append([track['name'], track['artists'][0]['name'], track['album']['images'][1]['url']])
	return allRecommendations

@app.route('/', methods=["GET", "POST"])
def index():
	result_rec = None
	if request.method == "POST":
		artist_from_search = request.form['qArtist']
		artist = get_artist(artist_from_search)
		if artist:
			result_rec = show_recommendations_for_artist(artist)
		else:
			return "Can't find that artist."
		return render_template('index.html', res=result_rec)
	return render_template('index.html', res=result_rec)

if __name__ == "__main__":
	app.run(debug=True)