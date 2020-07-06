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
username = ''
playerlist = 'spotify:playlist:560Qtov5uz9TSBSYj8hRPa'

def Top_Artists():
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
    df.plot(x = 'Artist', y='Songs', kind='barh')
    plt.show()

    top_artist = ""
    top_count = 0
    for artist in range(len(Data['Artist'])):
        if Data['Songs'][artist] > top_count:
            top_artist = Data['Artist'][artist]
            top_count = Data['Songs'][artist]
    print(top_artist)


#https://developer.spotify.com/documentation/web-api/reference/albums/get-album/
#https://developer.spotify.com/documentation/web-api/reference/object-model/#album-object-simplified
def Group_Year():
    results = sp.user_playlist_tracks(username, playerlist)
    tracks = results['items']
    fields = ['items,total']

    Years = {
        'Release Date': [],
        'Song Count': []
    }
    total_count = 0
    explicit_count = 0

    while total_count < results["total"]:
        for t in tracks:

            track_name = t['track']['name']
            track_artist = t['track']['artists'][0]['name']
            track_date = t['track']['album']['release_date']
            print(track_date)

            if track_date is None:
                continue

            if int(track_date[:4]) in Years['Release Date']:
                Years['Song Count'][Years['Release Date'].index(int(track_date[:4]))] += 1
            else:
                Years['Release Date'] += [int(track_date[:4])]
                Years['Song Count'] += [1]

            total_count += 1
        results = sp.user_playlist_tracks(username, playerlist, fields=fields, limit=100, offset=total_count)
        tracks = results['items']
        total_count += 1
        if total_count > 1500:
            break
    Years = Order_Years(Years)

    df = pandas.DataFrame(Years, columns=['Release Date', 'Song Count'])
    df.plot(x='Release Date', y='Song Count', kind='bar')
    plt.show()

#Orders a given Dataset of release dates of songs in ascending order
def Order_Years(given_years):
    years = given_years['Release Date']
    s_count = given_years['Song Count']
    n_years = sorted(years)
    new_s_count = []
    for i in range(len(years)):
        new_s_count += [s_count[years.index(n_years[i])]]

    new_years = {
        'Release Date':n_years,
        'Song Count':new_s_count
    }
    return new_years


#https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/
def Explicit_Percent():
    results = sp.user_playlist_tracks(username, playerlist)
    tracks = results['items']
    fields = ['items,total']

    Explicit_Songs_Index = {
        'Artist': [],
        'Song': []
    }
    total_count = 0
    explicit_count = 0

    while total_count < results["total"]:
        for t in tracks:

            track_id = t['track']['id']
            track_name = t['track']['name']
            track_artist = t['track']['artists'][0]['name']

            if t['track']['explicit']:
                print(track_name)
                if track_artist in Explicit_Songs_Index['Artist']:
                    a_index = Explicit_Songs_Index['Artist'].index(track_artist)
                    Explicit_Songs_Index['Song'][a_index] += [track_name]
                else:
                    Explicit_Songs_Index['Artist'] += [track_artist]
                    Explicit_Songs_Index['Song'] += [[track_name]]
                explicit_count += 1

            total_count += 1
        results = sp.user_playlist_tracks(username, playerlist, fields=fields, limit=100, offset=total_count)
        tracks = results['items']
        total_count += 1
        if total_count > 1500:
            break

    graph_data = {
        'Song type': ['Not explicit', 'Explicit'],
        'Amount': [total_count - explicit_count, explicit_count]
    }
    df = pandas.DataFrame(graph_data, columns=['Song type', 'Amount'])
    df.plot(x='Song type', y='Amount', kind='bar')
    plt.show()
    print(str(total_count) + ' ' + str(explicit_count))

#https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
def User_Favourites():
    print('x')


#Explicit_Percent()
#Top_Artists()

#Group_Year()


