import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
import pandas as pd
import pdb

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Magic Bronson'

client_id = "your_client_id"
client_secret = "your_client_secret"

client_credentials_manager = SpotifyClientCredentials(client_id="fac9c94efcc04895b83bd73aa53bbbf8",
                                                      client_secret="15a3224aa35242cba201e933284aedc5")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# result = sp.search(search_str)
# pprint.pprint(len(result))

# for i in sp.artist_related_artists("3WrFJ7ztbogyGnTHbHJFl2")['artists']:
#     print(i['id'],i['name'],i['followers'],i['href'],sep=' === ')
#





t = sp.search(q='genre:rock', type='artist', limit=10)
for i in t["artists"]["items"]:
    print(i["name"])










# artist_name = []
# track_name = []
# popularity = []
# track_id = []
# related = []
# for i in range(0, 10, 50):
#     track_results = sp.search(q='genre:rock', type='artist', limit=10, offset=i)
#     print(type(track_results['artists'].values()))
#     for i, k in track_results['artists'].items():
#         print()
        # artist_name.append(t['artists'][0]['name'])
        # track_name.append(t['name'])
        # track_id.append(t['id'])
        # popularity.append(t['popularity'])
        # related.append((sp.artist_related_artists(t['id'])))
        # print(t['id'])

# track_dataframe = pd.DataFrame(
#     {'artist_name': artist_name, 'track_name': track_name, 'track_id': track_id, 'popularity': popularity})
# print(track_dataframe.shape)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(track_dataframe)
# pdb.set_trace()
