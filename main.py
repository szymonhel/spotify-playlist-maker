from bs4 import BeautifulSoup
import spotipy
import os
import requests
from datetime import datetime

date_of_playlist = datetime.strptime(input("Pass date in format YYYY-MM-DD: "), '%Y-%m-%d')
html_site = requests.get(f"https://www.billboard.com/charts/hot-100/{date_of_playlist.date()}")
html_text = html_site.text

soup = BeautifulSoup(html_text, "html.parser")

title_html = [header.getText().replace("\n",  "").replace("\t",  "") for header in soup.select("ul li h3#title-of-a-story")]

os.environ["SPOTIPY_CLIENT_ID"] = ""
os.environ["SPOTIPY_CLIENT_SECRET"] = ""
os.environ["SPOTIPY_REDIRECT_URI"] = "http://example.com"

spotify = spotipy.SpotifyOAuth(scope="playlist-modify-private", show_dialog=True,
        cache_path="token.txt")

sp = spotipy.Spotify(oauth_manager=spotify)

song_uris = []

for title in title_html:
        url = f"track:{title} year:{date_of_playlist.year}"
        try:
                result = sp.search(url, type="track")
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
        except:
                print("ERROR")

playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=f"{date_of_playlist.date()} Billboard 100", public=False)

print(playlist)

sp.playlist_add_items(playlist["id"], song_uris)
print(song_uris)

