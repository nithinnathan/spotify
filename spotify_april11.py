#region PACKAGES

from os import environ
from sys import stdout
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import argparse

#endregion

#region CLASSES & VARIABLES

# os variables
environ["SPOTIPY_CLIENT_ID"]        = "2bfc1a2c59684012abbad70a5b207f68";
environ["SPOTIPY_CLIENT_SECRET"]    = "e037fc043e68407fa34155238486910d";
environ["SPOTIPY_REDIRECT_URI"]     = "http://example.com";

# spotify api client
scope = 'user-library-read user-library-modify playlist-read-private playlist-modify-private user-top-read user-read-currently-playing'
sp = Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout=60)

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('album_uri', help="find using 3 dots + share + option; wrap arg in double quotes")
parser.add_argument("-s", "--save", action="store_true", help="do you want to save these songs to a playlist?")
args = parser.parse_args()

# new playlists
hard_hits_playlist  = 'spotify:playlist:7zZ91jqOWdF7D9piIj47qq'
bangers_playlist    = 'spotify:playlist:5q2ADIHQBaavTrawdRWqhY'
chill_hits_playlist = 'spotify:playlist:08Dlybd42dWGnqkLDql6b8'

# status flag
can_proceed = True

# colors for terminal output
class TerminalColors:
    BRPURPLE    = '\u001b[30;1m'
    BRRED       = '\u001b[31;1m'
    BRGREEN     = '\u001b[32;1m'
    BRYELLOW    = '\u001b[33;1m'
    BRDBLUE     = '\u001b[34;1m'
    BRMAROON    = '\u001b[35;1m'
    BRLBLUE     = '\u001b[36;1m'
    BRWHITE     = '\u001b[37;1m'
    # BGBRPURPLE  = '\u001b[40;1m'
    # BGBRRED     = '\u001b[41;1m'
    # BGBRGREEN   = '\u001b[42;1m'
    # BGBRYELLOW  = '\u001b[43;1m'
    # BGBRDBLUE   = '\u001b[44;1m'
    # BGBRMAROON  = '\u001b[45;1m'
    ENDC        = '\033[0m'

#endregion

#region DEFINITIONS

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def find_songs(album_uri):
        
    # declare attribute lists
    hard_saved_track_uri        = []
    bangers_saved_track_uri     = []
    chill_hits_saved_track_uri  = []

    # get interested album
    tracks = sp.album_tracks(album_uri)
        
    # get track uri from album
    track_uri = [t["uri"] for t in tracks["items"]]

    # determine bangers and chill hits
    for tu in track_uri:
        features = sp.audio_features(tracks=[tu])
        if features[0]["acousticness"] <= 0.01:
            hard_saved_track_uri.append(tu)
        elif features[0]["acousticness"] > 0.01 and features[0]["acousticness"] <= 0.2:
            bangers_saved_track_uri.append(tu)
        else:
            chill_hits_saved_track_uri.append(tu)
            
    # return chosen songs
    return hard_saved_track_uri, bangers_saved_track_uri, chill_hits_saved_track_uri
         
def print_info(album_uri, saved_track_uri, analysis_type):
    
    # get album and artist names
    album_name  = sp.album(album_uri)["name"]
    artist_name = sp.album(album_uri)["artists"][0]["name"]
    
    #stdout.flush()
    
    # print album logistic info
    if (analysis_type == "Hard Hits"):
        playlist = hard_hits_playlist
        stdout.write(f"\nFinding {TerminalColors.BRLBLUE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
    elif (analysis_type == "Bangers"):
        playlist = bangers_playlist
        stdout.write(f"\nFinding {TerminalColors.BRDBLUE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
    elif (analysis_type == "Chill Hits"):
        playlist = chill_hits_playlist
        stdout.write(f"\nFinding {TerminalColors.BRPURPLE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
    else:
        playlist = None
    
    #stdout.flush()
    
    # print number of found songs
    if len(saved_track_uri) == 0:
        stdout.write(f"{TerminalColors.BRRED}Found 0 Songs!\n{TerminalColors.ENDC}")
    elif len(saved_track_uri) == 1:
        stdout.write(f"{TerminalColors.BRGREEN}Found 1 Song!{TerminalColors.ENDC}")
        stdout.flush()
        print('\n')
    else:
        stdout.write(f"{TerminalColors.BRGREEN}Found {len(saved_track_uri)} Songs!{TerminalColors.ENDC}")
        stdout.flush()
        print('\n')
    
    # print track names
    if len(saved_track_uri) > 0:
        for (o, p) in enumerate(saved_track_uri, start=1):
            track = sp.track(p)
            print(str(o) + ". " + track["name"])

    # save tracks to playlist
    if len(saved_track_uri) > 0 and args.save:
        sp.playlist_add_items(playlist, saved_track_uri)

#endregion

#region LOGIC

# error handling for command line args
if (len(args.album_uri) != 36 and len(args.album_uri) != 39) or (args.album_uri[0:14] != "spotify:album:" and args.album_uri[0:17] != "spotify:playlist:"):
    print(f"\n{TerminalColors.BRRED}Not a valid URI. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
    can_proceed = False

# album analysis preprocessing
if args.album_uri[0:14] == "spotify:album:":
    all_album_uri = [args.album_uri]
    
# playlist analysis preprocessing
if args.album_uri[0:17] == "spotify:playlist:":
    all_albums = sp.playlist_items(args.album_uri)
    all_album_uri = [all_albums["items"][i]["track"]["album"]["uri"] for i in range(len(all_albums["items"]))]
    all_album_uri = remove_duplicates(all_album_uri)

# driver code
if can_proceed == True:
    for album_uri in all_album_uri:
        hard_hits, bangers, chill_hits = find_songs(album_uri)
        print_info(album_uri, hard_hits, "Hard Hits")
        print_info(album_uri, bangers, "Bangers")
        print_info(album_uri, chill_hits, "Chill Hits")
    
#endregion
