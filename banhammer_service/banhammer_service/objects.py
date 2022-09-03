from typing import Any


class Response(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if self.get(__name):
            self[__name] = __value
        else:
            super().__setattr__(__name, __value)


class Playlist(Response):
    def filter_playlist(self):
        pass

    def delete_playlist(self):
        pass

    def duplicate_playlist(self):
        pass


class Tracklist(Response):
    @property
    def tracks(self):
        return [Track(i['track']) for i in self['items'] if i.get('track')]


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
