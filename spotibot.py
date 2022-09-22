import urllib.request
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube,Playlist
import os

client_credentials_manager = SpotifyClientCredentials(client_id='e5219f38064d490e8b7b3231e092287c', client_secret='1852a968e7f9484c85f97090226071c1')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def find_link(name):
    query = name.split(' ')
    srch = ''
    for i in query:
        srch = srch+'+'+i
    srch = srch[1:]
    print(srch)
    url = str(f'https://www.youtube.com/results?search_query={srch}')
    url = url.encode('ascii', 'ignore').decode('ascii')

    html = urllib.request.urlopen(url)
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    return ('https://www.youtube.com/watch?v='+video_ids[0])



def download_spotify_songs(playlistlink,name):
    playlist_link = playlistlink
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        track_name = track["track"]["name"]
        
        artist_name = track["track"]["artists"][0]["name"]
        if f'{track_name}.mp3' in os.listdir('\\songs'):
            continue
        link = find_link(str(track_name+artist_name))
        yt = YouTube(link)
        try:
            yt.streams.get_audio_only().download(filename=f'{track_name}.mp3',output_path=f'\\songs\\{name}')
        except OSError:
            yt.streams.get_audio_only().download(filename=f'{track_name[0:4]}.mp3',output_path=f'\\songs\\{name}')
        print('downloaded')

def download_yt_songs(playlist,name):
    p = Playlist(playlist)
    for i in p.videos:
        i.streams.get_highest_resolution().download(output_path = f'\\videos\\{name}')
        print('downloaded')
    
print("Welcome to TH3 D0WN704D3R")
print('What do you want to download?')
print('1)spotify playlist or 2)youtube playlist')
job = int(input('1 or 2'))
if job == 1:
    print('enter spotify playlist link')
    plink = input()
    name = input('What do you wanna name the playlist?')
    download_spotify_songs(plink,name)
elif job == 2:
    print('enter yt playlist link')
    plink = input()
    name = input('What do you wanna name the playlist?')
    download_yt_songs(plink,name)
else:
    print('invalid input')
    print('TRY AGAIN')





