#region PACKAGES

from os import environ
from sys import stdout
from argparse import ArgumentParser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import statistics
from operator import itemgetter
from scipy import stats
import math

#endregion

#region CLASSES & VARIABLES

# os variables
environ["SPOTIPY_CLIENT_ID"] = "2bfc1a2c59684012abbad70a5b207f68";
environ["SPOTIPY_CLIENT_SECRET"] = "e037fc043e68407fa34155238486910d";
environ["SPOTIPY_REDIRECT_URI"] = "http://example.com";

# spotify api client
scope = 'user-library-read user-library-modify playlist-read-private playlist-modify-private user-top-read user-read-currently-playing'
sp = Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout=60)

# parse command line arguments
parser = ArgumentParser()
parser.add_argument('album_uri', help="find using 3 dots + share + option; wrap arg in double quotes")
args = parser.parse_args()

# new playlists
banger_playlist = 'spotify:playlist:0pC8BVMPDK756trYEB103E'
chill_playlist = 'spotify:playlist:1ermkPd1s1aUC7FbjIuGDP'

# status flag
can_proceed = True

# colors for terminal output
class TerminalColors:
    ENDC        = '\033[0m'
    BRRED       = '\u001b[31;1m'
    BRGREEN     = '\u001b[32;1m'
    BRDBLUE     = '\u001b[34;1m'
    BRYELLOW    = '\u001b[33;1m'
    BRMAROON    = '\u001b[35;1m'
    BRPURPLE    = '\u001b[30;1m'

#endregion

#region DEFINITIONS

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def find_songs(album_uri):
        
    # declare attribute lists
    bangers_saved_track_uri = []
    chill_hits_saved_track_uri = []
    high_loudness = []
    low_loudness = []
    loudness = [high_loudness, low_loudness]
    calculate_means = []
    danceability_mean = []
    acousticness_mean = []
    popularity = []
    means = [danceability_mean, acousticness_mean]
    attributes = ["danceability", "acousticness"]

    # get interested album
    tracks = sp.album_tracks(album_uri)
    
    # return all tracks from single
    if sp.album(album_uri)["album_type"] == "single":
        for j in range(sp.album(album_uri)["total_tracks"]):
            bangers_saved_track_uri.append(tracks["items"][j]["uri"])
        return bangers_saved_track_uri
        
    # get track uri from album
    track_uri = [t["uri"] for t in tracks["items"]]# if t["duration_ms"] >= 60000]
                # and "skit" not in t["name"].lower()
                # and "speaks" not in t["name"].lower()
                # and "instrumental" not in t["name"].lower()
                # and "intro" not in t["name"].lower()
                # and "inter" not in t["name"].lower()
                # and "outro" not in t["name"].lower()
                # and "remix" not in t["name"].lower()]
    
    # get most popular song
    for x in track_uri:
        track = sp.track(x)
        features = sp.audio_features(tracks=[x])
        if track["popularity"] == 0 or track["popularity"] == None:
            continue
        else:
            popularity.append((features[0]["uri"], track["popularity"]))
    popular_uri = max(popularity, key=itemgetter(1))[0]
            
    # calculate loudness mean
    calculate_means = [sp.audio_features(tracks=[tu])[0]["loudness"] for tu in track_uri]
    loudness_mean = math.floor(float(statistics.fmean(calculate_means)))
    calculate_means.clear()
    
    # sort tracks based on loudness
    for tu in track_uri:
        features = sp.audio_features(tracks=[tu])
        high_loudness.append(tu) if features[0]["loudness"] >= loudness_mean else low_loudness.append(tu)
    
    # calculate danceability and acousticness means
    for l in loudness:
        for attr, m in zip(attributes, means):
            for tu in l:
                features = sp.audio_features(tracks=[tu])
                calculate_means.append(features[0][attr])
            m.append(float(statistics.fmean(calculate_means)))
            calculate_means.clear()
    
    # determine bangers and chill hits
    for l, dm, am in zip(loudness, danceability_mean, acousticness_mean):
        for tu in l:
            features = sp.audio_features(tracks=[tu])
            if features[0]["danceability"] >= dm and features[0]["acousticness"] <= am:
                bangers_saved_track_uri.append(tu)
            if features[0]["danceability"] <= dm and features[0]["acousticness"] >= am:
                chill_hits_saved_track_uri.append(tu)
    
    # add most popular song to bangers
    if len(popularity) > 0:
        bangers_saved_track_uri.append(popular_uri)
        bangers_saved_track_uri = remove_duplicates(bangers_saved_track_uri)
    
    # return chosen songs
    return bangers_saved_track_uri, chill_hits_saved_track_uri
    
def print_info(album_uri, saved_track_uri, analysis_type):
    
    # get album and artist names
    album_name = sp.album(album_uri)["name"]
    artist_name = sp.album(album_uri)["artists"][0]["name"]
    
    # print album logistic info
    if (analysis_type == "Bangers"):
        playlist = banger_playlist
        stdout.write(f"\nFinding {TerminalColors.BRDBLUE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
    elif (analysis_type == "Chill Hits"):
        playlist = chill_playlist
        stdout.write(f"\nFinding {TerminalColors.BRPURPLE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
    else:
        playlist = None
    stdout.flush()
    
    # print number of found songs
    if len(saved_track_uri) == 0:
        stdout.write(f"{TerminalColors.BRRED}Found 0 Songs!{TerminalColors.ENDC}")
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
    else:
        print(' ')

    # # save tracks to playlist
    # if len(saved_track_uri) > 0:
    #     sp.playlist_add_items(playlist, saved_track_uri)

#endregion

#region LOGIC

# error handling for command line args
if (len(args.album_uri) != 36 and len(args.album_uri) != 39) or (args.album_uri[0:14] != "spotify:album:" and args.album_uri[0:17] != "spotify:playlist:"):
    print(f"\n{TerminalColors.BRRED}Not a valid URI. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
    can_proceed = False

# album analysis preprocessing
if args.album_uri[0:14] == "spotify:album:":
    tracks = sp.album_tracks(args.album_uri)
    if tracks["total"] <= 2:
        print(f"\n{TerminalColors.BRRED}Need more songs to analyze. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
        can_proceed = False
    else:
        all_album_uri = [args.album_uri]
    
# playlist analysis preprocessing
if args.album_uri[0:17] == "spotify:playlist:":
    all_albums = sp.playlist_items(args.album_uri)
    all_album_uri = [all_albums["items"][i]["track"]["album"]["uri"] for i in range(len(all_albums["items"]))]
    all_album_uri = remove_duplicates(all_album_uri)

# driver code
if can_proceed == True:
    for album_uri in all_album_uri:
        bangers, chill_hits = find_songs(album_uri)
        chill_hits = [x for x in chill_hits if x not in bangers]
        print_info(album_uri, bangers, "Bangers")
        print_info(album_uri, chill_hits, "Chill Hits")
    
#endregion
