import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
import pandas as pd
import pdb
import re

# client_id = "fac9c94efcc04895b83bd73aa53bbbf8"
# client_secret = "15a3224aa35242cba201e933284aedc5"

client_credentials_manager = SpotifyClientCredentials(client_id="CLIENT_ID_HERE",
                                                      client_secret="CLIENT_SECRET_HERE")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def getRelated(id):
    label = []
    popularity = []
    followers = []
    ids = []

    for i in sp.artist_related_artists(id)['artists']:
        # print(i['id'],i['name'],i['followers'],i['href'],sep=' === ')
        label.append(i['name'])
        followers.append(i['followers']["total"])
        ids.append(i['id'])
        popularity.append(i["popularity"])

        dataf = pd.DataFrame(
            {'Id': ids,
             'Label': label,
             "Followers": followers,
             'Popularity': popularity}
        )
        # print(dataf)

    return dataf


class Node():
    def __init__(self, id, name):
        self.id = id
        self.name = name.replace(",", " ")
        self.popularity = 0
        self.followers = 0
        self.related = None

    def setRelated(self, related):
        self.related = related

# ------------------------------------------------------------------------------------------------------------------


def isExist(list, id):
    for i in list:
        if i.id == id:
            return i
    return None


rel = list()
rel_d = dict()

norel = list()

edgy = list()
nodes = list()


def search(id, name, depth):
    print(depth * '      ', '|', (depth - 1) * '------', '>', name, sep='')

    depth += 1
    isEdge = isExist(edgy, id)

    if isEdge:
        return

    if depth > branching:
        if not isExist(nodes, id):
            artist = Node(id, name)
            nodes.append(artist)
        return

    artist = Node(id, name)
    df = getRelated(id)
    artist.related = df

    edgy.append(artist)
    if not isExist(nodes, id):
        nodes.append(artist)

    for index, row in artist.related.iterrows():
        if row['Followers'] > min:
            search(row['Id'], row['Label'], depth)


sID = input("ID: ")
sName = input("Name: ")

min = int(input("--Minimum followers: "))
branching = int(input("--Branching: "))

search(sID, sName, 0)

for i in edgy:
    for index, row in i.related.iterrows():
        exist = isExist(nodes, row["Id"])
        if exist:
            exist.followers = row['Followers']
            exist.popularity = row["Popularity"]


nodefile = open("dots.csv", "w+")
nodefile.write(u'\ufeff')
nodefile.write("Id,Label,Popularity,Followers\n")

for artist in nodes:
    txt = [artist.id, artist.name, artist.popularity, artist.followers]
    txt = [str(i) for i in txt]
    nodefile.write(','.join(txt) + '\n')
nodefile.close()


edges = open("lines.csv", "w+")
edges.write(u'\ufeff')
edges.write('Source,Target,Type\n')

for artist in edgy:
    for index, row in artist.related.iterrows():
        txt = [artist.id, row['Id'], 'Undirected']
        txt = [str(i) for i in txt]
        edges.write(','.join(txt) + '\n')
edges.close()

print("edge.csv and lines.csv has been saved into directory!")
