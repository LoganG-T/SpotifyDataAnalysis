#Group all artists in a playlist / list of playlists and display the results

#

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas
import matplotlib.pyplot as plt

#Spotify developer account details
CLIENT_ID = ''
CLIENT_SECRET = ''

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))


#Users spotify userID and the ID of the users playlist (Only public playlists available)
username = 'bar7taody2urtwo3m3rpkbd9q'
playerlist = 'spotify:playlist:560Qtov5uz9TSBSYj8hRPa'
results = sp.user_playlist_tracks(username, playerlist)
tracks = results['items']

fields = ['items,total']

Data = {
        'Artist' : [],
        'Songs' : []
        }
track_count = 0

#Adds all tracks from a chosen playlist into a data list
while track_count < results["total"]:
    for t in tracks:

        track_id = t['track']['id']
        track_name = t['track']['name']
        track_artist = t['track']['artists'][0]['name']

        print(track_id + ' ' + track_name + ' ' + track_artist)

        if track_artist in Data['Artist']:
            a_index =  Data['Artist'].index(track_artist)
            Data['Songs'][a_index] += 1
        else:
            Data['Artist'] += [track_artist]
            Data['Songs'] += [1]

        track_count += 1
    results = sp.user_playlist_tracks(username, playerlist, fields=fields, limit=100, offset=track_count)
    tracks = results['items']
    if track_count > 200:
        break

DisplayData = {
        'Artist' : [],
        'Songs' : []
        }


def Find_Top_Ten():
    top_ten = [1 for i in range(10)]
    for i in range(len(Data['Artist'])):
        if Data['Songs'][i] > min(top_ten):
            top_ten[top_ten.index(min(top_ten))] = Data['Songs'][i]
    return min(top_ten)



for i in range(len(Data['Artist'])):
    if Data['Songs'][i] >= Find_Top_Ten():
        DisplayData['Artist'] += [Data['Artist'][i]]
        DisplayData['Songs'] += [Data['Songs'][i]]

df = pandas.DataFrame(DisplayData,columns=['Artist','Songs'])
df.plot(x = 'Artist', y='Songs', kind='bar')
plt.show()

top_artist = ""
top_count = 0
for artist in range(len(Data['Artist'])):
    if Data['Songs'][artist] > top_count:
        top_artist = Data['Artist'][artist]
        top_count = Data['Songs'][artist]
print(top_artist)


