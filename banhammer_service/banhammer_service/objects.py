from typing import Any

class Response(dict):
    def __getattr__(self, item):
        return self.get(item)

class Playlist(Response):
    def filter_playlist(self):
        pass

    def delete_playlist(self):
        pass

    def duplicate_playlist(self):
        pass

class Track(Response):
    @property
    def artists(self):
        return [Artist(i) for i in self['artists']]

    def add_track(self):
        pass

    def delete_track(self):
        pass

    def ban_track(self):
        pass

    def unban_track(self):
        pass



class Artist(Response):
    def add_(self):
        pass
    
    def delete_(self):
        pass
    
    def ban_(self):
        pass
    
    def unban_(self):
        pass
