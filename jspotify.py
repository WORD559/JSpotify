##Spotify API Library
#This should be fun.

import requests, sys, os

class PlatformError(Exception):
    pass

class Track(object):
    def __init__(self,json):
        self.__url__ = "https://api.spotify.com"
        self.name = json["name"]
        self.external_urls = json["external_urls"]
        self.url = json["external_urls"]["spotify"]
        self.uri = json["uri"]
        self.id = json["id"]
        self.duration = json["duration_ms"]
        self.track_number = json["track_number"]
        self.disc_number = json["disc_number"]
        self.explicit = json["explicit"]
        self.preview_url = json["preview_url"]
        if json["album"] != None:
            self.album = Album(json["album"])
        else:
            self.album = None
        if json["artists"]  != None:
            self.artists = [Artist(x) for x in json["artists"]]
        else:
            self.artists = None

    def open(self):
        if sys.platform == "win32":
            os.system("start "+self.uri)
        else:
            raise PlatformError("Can only open in Spotify on Windows.")

    def __str__(self):
        return self.name + " - " + " & ".join([str(x) for x in self.artists])

    def __repr__(self):
        return "Track('"+self.name+" - "+" & ".join([str(x) for x in self.artists])+"')"
    
class Artist(object):
    def __init__(self,json):
        self.__url__ = "https://api.spotify.com"
        self.name = json["name"]
        self.external_urls = json["external_urls"]
        self.url = json["external_urls"]["spotify"]
        self.uri = json["uri"]
        self.request_url = json["href"]
        self.id = json["id"]

    def open(self):
        if sys.platform == "win32":
            os.system("start "+self.uri)
        else:
            raise PlatformError("Can only open in Spotify on Windows.")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Artist('"+self.name+"')"
    
class Album(object):
    def __init__(self,json):
        self.__url__ = "https://api.spotify.com"
        self.name = json["name"]
        self.external_urls = json["external_urls"]
        self.url = json["external_urls"]["spotify"]
        self.uri = json["uri"]
        self.request_url = json["href"]
        self.art = json["images"][0]["url"]
        self.id = json["id"]
        if json["artists"]  != None:
            self.artists = [Artist(x) for x in json["artists"]]
        else:
            self.artists = None

    def open(self):
        if sys.platform == "win32":
            os.system("start "+self.uri)
        else:
            raise PlatformError("Can only open in Spotify on Windows.")

    def get_tracks(self):
        self.tracks = []
        total = 1
        n = self.__url__+"/v1/albums/%s/tracks" % self.id
        while len(self.tracks) < total:
            r = requests.get(n)
            j = r.json()
            total = int(j["total"])
            for x in j["items"]:
                x["artists"] = None
                x["album"] = None
                self.tracks.append(Track(x))
                self.tracks[-1].artists = self.artists
                self.tracks[-1].album = self
            n = j["next"]

    def __str__(self):
        return self.name + " - " + " & ".join([str(x) for x in self.artists])

    def __repr__(self):
        return "Album('"+self.name+" - "+" & ".join([str(x) for x in self.artists])+"')"

class Spotify(object):
    def __init__(self):
        self.s = requests.session()
        self.__url__ = "https://api.spotify.com"

    def search_albums(self,query):
        r = self.s.get(self.__url__+"/v1/search?type=album&q=%s" % query)
        j = r.json()
        print "Got "+str(j["albums"]["total"])+" albums"
        data = []
        for x in j["albums"]["items"]:
            data.append(Album(x))
            
        return data

    def search_tracks(self,query):
        r = self.s.get(self.__url__+"/v1/search?type=track&q=%s" % query)
        j = r.json()
        print "Got "+str(j["tracks"]["total"])+" tracks"
        data = []
        for x in j["tracks"]["items"]:
            data.append(Track(x))
            
        return data

    def search_artists(self,query):
        r = self.s.get(self.__url__+"/v1/search?type=artist&q=%s" % query)
        j = r.json()
        print "Got "+str(j["artists"]["total"])+" artists"
        data = []
        for x in j["artists"]["items"]:
            data.append(Artist(x))
            
        return data
