#region PACKAGES

from os import environ
from sys import stdout
from argparse import ArgumentParser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import statistics
from operator import itemgetter
from scipy import stats

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
    popularity = []
    calculate_loudness_mean = []
    # calculate_energy_mean = []
    calculate_acousticness_mean = []
    calculate_danceability_mean = []
    # calculate_instrumentalness_mean = []
    loudness_mean = 0
    # energy_mean = 0
    acousticness_mean = 0
    danceability_mean = 0
    # instrumentalness_mean = 0
    
    # calculate_liveness_mean = []
    # calculate_speechiness_mean = []
    # calculate_tempo_mean = []
    calculate_valence_mean = []
    # calculate_tempo_mean = []
    # liveness_mean = 0
    # speechiness_mean = 0
    # tempo_mean = 0
    valence_mean = 0
    # tempo_mean = 0

    # get interested album
    tracks = sp.album_tracks(album_uri)
    
    # return all tracks from single
    if sp.album(album_uri)["album_type"] == "single":
        for j in range(sp.album(album_uri)["total_tracks"]):
            bangers_saved_track_uri.append(tracks["items"][j]["uri"])
        return bangers_saved_track_uri, chill_hits_saved_track_uri
        
    # get track uri from album
    track_uri = [t["uri"] for t in tracks["items"] if t["duration_ms"] >= 60000]
    
    # calculate means
    for tu in track_uri:
        features = sp.audio_features(tracks=[tu])
        calculate_loudness_mean.append(features[0]["loudness"])
        # calculate_energy_mean.append(features[0]["energy"])
        calculate_acousticness_mean.append(features[0]["acousticness"])
        calculate_danceability_mean.append(features[0]["danceability"])
        # calculate_instrumentalness_mean.append(features[0]["instrumentalness"])
        # calculate_liveness_mean.append(features[0]["liveness"])
        # calculate_speechiness_mean.append(features[0]["speechiness"])
        # calculate_tempo_mean.append(features[0]["tempo"])
        calculate_valence_mean.append(features[0]["valence"])
        # calculate_tempo_mean.append(features[0]["tempo"])
    loudness_mean = statistics.quantiles(calculate_loudness_mean, n=10)
    # energy_mean = statistics.quantiles(calculate_energy_mean, n=10)
    acousticness_mean = statistics.quantiles(calculate_acousticness_mean, n=10)
    danceability_mean = statistics.quantiles(calculate_danceability_mean, n=10)
    # instrumentalness_mean = statistics.quantiles(calculate_instrumentalness_mean, n=10)
    # liveness_mean = statistics.quantiles(calculate_liveness_mean, n=10)
    # speechiness_mean = statistics.quantiles(calculate_speechiness_mean, n=10)
    # tempo_mean = statistics.quantiles(calculate_tempo_mean, n=10)
    valence_mean = statistics.quantiles(calculate_valence_mean, n=10)
    # tempo_mean = statistics.quantiles(calculate_tempo_mean, n=10)
    
    # determine bangers and chill hits
    for tu in track_uri:
        track = sp.track(tu)
        features = sp.audio_features(tracks=[tu])
        appropriate_names = ("skit" not in track["name"].lower() and
                             "speaks" not in track["name"].lower() and
                             "instrumental" not in track["name"].lower() and
                             "intro" not in track["name"].lower() and
                             "inter" not in track["name"].lower() and
                             "outro" not in track["name"].lower())# and
                             #"remix" not in track["name"].lower())
            
        if (appropriate_names and
            features[0]["danceability"] >= danceability_mean[3] and
            features[0]["acousticness"] <= acousticness_mean[5]):
            bangers_saved_track_uri.append(tu)
            
        if (appropriate_names and
            features[0]["danceability"] <= danceability_mean[5] and
            features[0]["acousticness"] >= acousticness_mean[3]):
            chill_hits_saved_track_uri.append(tu)
            
        if track["popularity"] == 0 or track["popularity"] == None:
            continue
        else:
            popularity.append((features[0]["uri"], track["popularity"]))
    
    # add most popular song to bangers
    if len(popularity) > 0:
        bangers_saved_track_uri.append(max(popularity, key=itemgetter(1))[0])
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

    # save tracks to playlist
    if len(saved_track_uri) > 0:
        sp.playlist_add_items(playlist, saved_track_uri)

#endregion

#region LOGIC

# error handling for command line args
if (len(args.album_uri) != 36 and len(args.album_uri) != 39) or (args.album_uri[0:14] != "spotify:album:" and args.album_uri[0:17] != "spotify:playlist:"):
    print(f"\n{TerminalColors.BRRED}Not a valid URI. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
    can_proceed = False

# album analysis preprocessing
if args.album_uri[0:14] == "spotify:album:":
    # tracks = sp.album_tracks(args.album_uri)
    # print(sp.album(args.album_uri))
    # if tracks["total"] <= 2:
    #     print(f"\n{TerminalColors.BRRED}Need more songs to analyze. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
    #     can_proceed = False
    # else:
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
