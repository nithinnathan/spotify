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

# colors for terminal output
class TerminalColors:
    ENDC        = '\033[0m'
    BGRED       = '\u001b[41;1m'
    BGGREEN     = '\u001b[42;1m'
    BGBLUE      = '\u001b[44;1m'
    BGYELLOW    = '\u001b[43;1m'
    BRRED       = '\u001b[31;1m'
    BRGREEN     = '\u001b[32;1m'
    BRLBLUE     = '\u001b[36;1m'
    BRDBLUE     = '\u001b[34;1m'
    BRYELLOW    = '\u001b[33;1m'
    BRMAROON    = '\u001b[35;1m'
    BRPURPLE    = '\u001b[30;1m'
    CGRAY       = '\u001b[38;5;240m'
    CWHITE      = '\u001b[38;5;255m'

#endregion



#region DEFINITIONS

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def find_songs(album_uri):
        
    # declare attribute lists
    bangers_saved_track_uri = []
    #chill_hits_saved_track_uri = []
    high_loudness = []
    low_loudness = []
    loudness = [high_loudness, low_loudness]
    calculate_means = []
    danceability_mean = []
    acousticness_mean = []
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
    track_uri = [t["uri"] for t in tracks["items"] if t["duration_ms"] >= 60000
                 and "skit" not in t["name"].lower()
                 and "speaks" not in t["name"].lower()
                 and "instrumental" not in t["name"].lower()
                 and "intro" not in t["name"].lower()
                 and "inter" not in t["name"].lower()
                 and "outro" not in t["name"].lower()
                 and "remix" not in t["name"].lower()]
            
    # calculate loudness mean
    calculate_means = [sp.audio_features(tracks=[tu])[0]["loudness"] * -1 for tu in track_uri]
    loudness_mean = statistics.harmonic_mean(calculate_means) * -1
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
            m.append(statistics.harmonic_mean(calculate_means))
            calculate_means.clear()
    
    # determine bangers
    for l, dm, am in zip(loudness, danceability_mean, acousticness_mean):
        popularity = []
        for tu in l:
            features = sp.audio_features(tracks=[tu])
            if features[0]["danceability"] >= dm and features[0]["acousticness"] <= am:
                bangers_saved_track_uri.append(tu)
                
            track = sp.track(tu)
            if track["popularity"] == 0 or track["popularity"] == None:
                continue
            else:
                popularity.append((features[0]["uri"], track["popularity"]))
            
            if len(popularity) > 0:
                bangers_saved_track_uri.append(max(popularity, key=itemgetter(1))[0])
            bangers_saved_track_uri = remove_duplicates(bangers_saved_track_uri)
        
        # # chill hits
        # if s == 1:
            
        #     # calculate loudness mean
        #     calculate_means = [sp.audio_features(tracks=[tu])[0]["loudness"] for tu in track_uri]
        #     loudness_mean = statistics.fmean(calculate_means)
        #     calculate_means.clear()
            
        #     # sort tracks based on loudness
        #     for tu in track_uri:
        #         features = sp.audio_features(tracks=[tu])
        #         high_loudness.append(tu) if features[0]["loudness"] >= loudness_mean else low_loudness.append(tu)
            
        #     # calculate danceability and acousticness means
        #     for l in loudness:
        #         for attr, m in zip(attributes, means):
        #             for tu in l:
        #                 features = sp.audio_features(tracks=[tu])
        #                 calculate_means.append(features[0][attr])
        #             #print(statistics.fmean(calculate_means))
        #             m.append(statistics.fmean(calculate_means))
        #             calculate_means.clear()
            
        #     # determine chill hits
        #     for l, dm, am in zip(loudness, danceability_mean, acousticness_mean):
        #         for tu in l:
        #             features = sp.audio_features(tracks=[tu])
        #             if features[0]["danceability"] <= dm and features[0]["acousticness"] >= am:
        #                 chill_hits_saved_track_uri.append(tu)
                
    # return chosen songs
    return bangers_saved_track_uri

def find_chill_songs(album_uri):
        
    # declare attribute lists
    bangers_saved_track_uri = []
    chill_hits_saved_track_uri = []
    high_loudness = []
    low_loudness = []
    loudness = [high_loudness, low_loudness]
    calculate_means = []
    danceability_mean = []
    acousticness_mean = []
    means = [danceability_mean, acousticness_mean]
    attributes = ["danceability", "acousticness"]

    # get interested album
    tracks = sp.album_tracks(album_uri)
        
    # get track uri from album
    track_uri = [t["uri"] for t in tracks["items"] if t["duration_ms"] >= 60000
                 and "skit" not in t["name"].lower()
                 and "speaks" not in t["name"].lower()
                 and "instrumental" not in t["name"].lower()
                 and "intro" not in t["name"].lower()
                 and "inter" not in t["name"].lower()
                 and "outro" not in t["name"].lower()]
        
    # calculate loudness mean
    calculate_means = [sp.audio_features(tracks=[tu])[0]["loudness"] for tu in track_uri]
    loudness_mean = statistics.fmean(calculate_means)
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
            #print(statistics.fmean(calculate_means))
            m.append(statistics.fmean(calculate_means))
            calculate_means.clear()
    
    # determine bangers
    for l, dm, am in zip(loudness, danceability_mean, acousticness_mean):
        popularity = []
        for tu in l:
            
            features = sp.audio_features(tracks=[tu])
            if features[0]["danceability"] >= dm and features[0]["acousticness"] <= am:
                bangers_saved_track_uri.append(tu)
                
            track = sp.track(tu)
            if track["popularity"] == 0 or track["popularity"] == None:
                continue
            else:
                popularity.append((features[0]["uri"], track["popularity"]))
            
            if len(popularity) > 0:
                bangers_saved_track_uri.append(max(popularity, key=itemgetter(1))[0])
                bangers_saved_track_uri = remove_duplicates(bangers_saved_track_uri)
    
    # determine chill hits
    for l, dm, am in zip(loudness, danceability_mean, acousticness_mean):
        for tu in l:
            features = sp.audio_features(tracks=[tu])
            if features[0]["danceability"] <= dm and features[0]["acousticness"] >= am:
                chill_hits_saved_track_uri.append(tu)
                
    # return chosen songs
    return chill_hits_saved_track_uri
    
def print_info(analysis_type, album_uri, saved_track_uri):
    
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
    #     #print(saved_track_uri)
    #     sp.playlist_add_items(playlist, saved_track_uri)

#endregion



#region LOGIC

# status flag
can_proceed = True

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
    #all_album_uri = []
    all_albums = sp.playlist_items(args.album_uri)
    all_album_uri = [all_albums["items"][i]["track"]["album"]["uri"] for i in range(len(all_albums["items"]))]
    # for i in range(len(all_albums["items"])):
    #     # if all_albums["items"][i]["track"]["album"]["album_type"] == "single":
    #     #     tracks = sp.album_tracks(all_albums["items"][i]["track"]["album"]["uri"])
    #     #     for j in range(all_albums["items"][i]["track"]["album"]["total_tracks"]):
    #     #         sp.playlist_add_items(banger_playlist, [tracks["items"][j]["uri"]])
    #     # else:
    #     all_album_uri.append(all_albums["items"][i]["track"]["album"]["uri"])
            
    #     # code for analyzing a playlist for bangers and chill hits
    #     #print(all_albums["items"][i]["track"]["uri"])
    #     #all_album_uri.append(all_albums["items"][i]["track"]["uri"])
        
    all_album_uri = remove_duplicates(all_album_uri)

# driver code
if can_proceed == True:
    for album_uri in all_album_uri:
        bangers = find_songs(album_uri)
        #chill_hits = find_chill_songs(album_uri)
        #actual_chill_hits = [x for x in chill_hits if x not in bangers]
        print_info("Bangers", album_uri, bangers)
        #print_info("Chill Hits", album_uri, actual_chill_hits)
    
#endregion



#region UNUSED CODE

# # get list of albums
# all_albums = sp.playlist_items('spotify:playlist:37i9dQZF1DXaxIqwkEGFEh')
# for i in range(len(all_albums["items"])):
#     # if all_albums["items"][i]["track"]["album"]["album_type"] == 'single':
#     #     continue
#     # all_album_uri.append(all_albums["items"][i]["track"]["album"]["uri"])
#     #print(all_albums["items"][i]["track"]["uri"])
#     all_album_uri.append(all_albums["items"][i]["track"]["uri"])
# all_album_uri = list(set(all_album_uri))

# # declare attribute lists
# uri = []
# saved_uri = []
# popularity = []
# low_loudness = []
# high_loudness = []
# loudness = [low_loudness, high_loudness]
# calculate_loudness_mean = []
# calculate_danceability_mean = []
# calculate_acousticness_mean = []
# loudness_mean = []
# danceability_mean = []
# acousticness_mean = []
# attributes = ["danceability", "acousticness"]
# calculate_means = [calculate_danceability_mean, calculate_acousticness_mean]
# means = [danceability_mean, acousticness_mean]
    
# # determine loudness mean
# for d in all_album_uri:
#     features = sp.audio_features(tracks=[d])
#     calculate_loudness_mean.append(features[0]["loudness"])
# loudness_mean.append(statistics.mean(calculate_loudness_mean))

# # sort tracks based on loudness
# for z in all_album_uri:
#     features = sp.audio_features(tracks=[z])
#     if features[0]["loudness"] < loudness_mean[0]:
#         low_loudness.append(z)
#     else:
#         high_loudness.append(z)

# # calculate danceability and acousticness means
# for f in loudness:
#     for g, h, m in zip(attributes, calculate_means, means):
#         for z in f:
#             features = sp.audio_features(tracks=[z])
#             h.append(features[0][g])
#         m.append(statistics.mean(h))
#         h.clear()

# # determine potential bangers
# for k, c, d in zip(loudness, danceability_mean, acousticness_mean):
#     for a in k:
#         features = sp.audio_features(tracks=[a])
#         track = sp.track(a)
#         if features[0]["danceability"] >= c and features[0]["acousticness"] <= d:
#             saved_uri.append(a)
#         if track["album"]["release_date"] >= date.today().strftime("%Y-%m-%d"):
#             continue
#         else:
#             popularity.append((features[0]["uri"], track["popularity"]))

# # sort songs by popularity
# if len(popularity) > 0:
#     sorted_popularity = sorted(popularity, key=lambda x: x[1], reverse=True)

# # # add 1 of top 3 popular songs from album if not picked up by algorithm
# # h = 0
# # if len(sorted_popularity) >= 3:
# #     while h < 3:
# #         if sorted_popularity[h][0] in saved_uri:
# #             h = h + 1
# #             continue
# #         else:
# #             saved_uri.append(sorted_popularity[h][0])
# # saved_uri = list(set(saved_uri))

# # remove duplicates
# # seen = set()
# # seen_add = seen.add
# # potential_bangers = [x for x in saved_uri if not (x in seen or seen_add(x))]

# # print track names
# # for i in saved_uri:
# #     features = sp.audio_features(tracks=[i])
# #     track = sp.track(i)
# #     print(track["name"])

# # save tracks to playlist
# sp.playlist_add_items(playlist, saved_uri)

# # print success message
# print('--------------------')
# print('Success!')

#endregion
