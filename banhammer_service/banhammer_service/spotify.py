from typing import Dict, List, Union
import spotipy
import logging
logger = logging.getLogger("BanHammer")

def find_playlist_by_name(session:spotipy.Spotify, name:str) -> Union[Dict, None]:
    playlists = session.current_user_playlists()
    while True:
        for playlist in playlists['items']:
            if name == playlist['name']:
                return playlist

        playlists = session.next(playlists)
        if not playlists:
            return None


def load_ban_list(file: str) -> Dict:
    banned_artists = {}
    with open(file, 'rt', encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            artist, id = line.split(',')
            banned_artists[id.strip()] = artist.strip()
    return banned_artists

def add_entry_to_banlist(file:str, name, id) -> None:
    with open(file, 'a+', encoding="UTF-8") as f:
        f.write(f"{name},{id}\n")


def filter_playlist(playlist: Dict, ban_list) -> None:
    removal_list = []
    # <listing all tracks here>
    for idx, entry in enumerate(playlist['items']):
        track_artists = entry['track']['artists']
        for artist in track_artists:  # <perform artist check here>
            if artist['id'] in ban_list:
                print(f"Removing entry for {artist['name']} - {artist['id']}")
                removal_list.append(idx)
    for idx in removal_list:
        del playlist['items'][idx]
    return playlist


def clear_playlist(session:spotipy.Spotify, playlist) -> None:
    track_id_list = []
    tracks = session.playlist_items(playlist['id'])
    while True:
        for item in tracks['items']:
            track_id_list.append(item['track']['uri'])
        tracks = session.next(tracks)
        if not tracks:
            break

    for track_chunk in chunk_generator(track_id_list, 100):
        session.playlist_remove_all_occurrences_of_items(
            playlist['id'], track_chunk)


def rebuild_playlist(session:spotipy.Spotify, playlist_id, playlist):
    rebuild_list = []
    for item in playlist['items']:
        rebuild_list.append(item['track']['uri'])

    for track_chunk in chunk_generator(rebuild_list, 100):
        session.playlist_add_items(playlist_id, track_chunk)


def chunk_generator(lst, n) -> List:
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def sanitize_new_music_friday(session:spotipy.Spotify, ban_list_file):
    ban_list = load_ban_list(ban_list_file)
    playlist = session.playlist_items(find_playlist_by_name(session,
        'New Music Friday')['id'], market='US')
    cleaned_playlist = find_playlist_by_name(session,'Better New Music Friday')
    clear_playlist(session, cleaned_playlist)
    rebuild_playlist(session, cleaned_playlist['id'],
                     filter_playlist(playlist, ban_list))

def remove_song_from_playlist(session:spotipy.Spotify, playlist_uri, song_uri):
    try:
        session.playlist_remove_all_occurrences_of_items(playlist_uri, song_uri)
    except spotipy.SpotifyException as e:
            logging.info(e.args)

def ban_current_playing_song(session:spotipy.Spotify, ban_file:str):
    current = session.current_playback()
    if current:
        name, id = (current['item']['name'], current['item']['id'])
        logger.info(f"banning {name}, {id}")
        if current['context']['type']=='playlist':
            _,_, context_id = current['context']['uri'].split(":")
            remove_song_from_playlist(session,context_id,[id])
        add_entry_to_banlist(ban_file, name, id)
        session.next_track()
    
def ban_current_playing_artist(session:spotipy.Spotify, ban_file:str):
    current = session.current_playback()
    if current:
        name, id, song_id = (current['item']['artists'][0]['name'], current['item']['artists'][0]['id'], current['item']['id'])
        logger.info(f"banning {name}, {id}")
        if current['context']['type']=='playlist':
            _,_, context_id = current['context']['uri'].split(":")
            remove_song_from_playlist(session,context_id,[song_id])
        add_entry_to_banlist(ban_file, name, id)
        session.next_track()