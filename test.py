#region PACKAGES

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import statistics
import argparse
from datetime import date
import sys

#endregion



#region CLASSES & VARIABLES

# os variables
os.environ["SPOTIPY_CLIENT_ID"] = "2bfc1a2c59684012abbad70a5b207f68";
os.environ["SPOTIPY_CLIENT_SECRET"] = "e037fc043e68407fa34155238486910d";
os.environ["SPOTIPY_REDIRECT_URI"] = "http://example.com";

# spotify api client
scope = 'user-library-read user-library-modify playlist-read-private playlist-modify-private user-top-read user-read-currently-playing'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), requests_timeout=60)

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('album_uri', help="find using 3 dots + share + option; wrap arg in double quotes")
args = parser.parse_args()

banger_playlist = 'spotify:playlist:0pC8BVMPDK756trYEB103E'

# if args.album_uri[0:17] == "spotify:playlist:":
#     all_album_uri = []
#     all_albums = sp.playlist_items(args.album_uri)
#     for i in range(len(all_albums["items"])):
#         #if all_albums["items"][i]["track"]["album"]["total_tracks"] <= 1:
#         print(all_albums["items"][i]["track"]["uri"])
#         print('\n')
#             #sp.playlist_add_items(banger_playlist, all_albums["items"][i]["track"]["album"]["uri"])

if args.album_uri[0:17] == "spotify:playlist:":
    all_album_uri = []
    all_albums = sp.playlist_items(args.album_uri)
    for i in range(len(all_albums["items"])):
        #if all_albums["items"][i]["track"]["album"]["total_tracks"] <= 1:
        # print(all_albums["items"][i]["track"]["album"]["uri"])
        # print('\n')
        #print(all_albums["items"][i]["track"]["album"]["album_type"])
        totaltracks = all_albums["items"][i]["track"]["album"]["total_tracks"]
        tracks = sp.album_tracks(all_albums["items"][i]["track"]["album"]["uri"])
        for j in range(totaltracks):
            print(tracks["items"][j]["uri"])
            print('\n')
            #sp.playlist_add_items(banger_playlist, [all_albums["items"][i]["track"]["uri"]])


#whatthe = ["spotify:track:4jtyUzZm9WLc2AdaJ1dso7"]

#sp.playlist_add_items(banger_playlist, whatthe)

# # new playlists
# banger_playlist = 'spotify:playlist:0pC8BVMPDK756trYEB103E'
# chill_playlist = 'spotify:playlist:1ermkPd1s1aUC7FbjIuGDP'

# # colors for terminal output
# class TerminalColors:
#     ENDC        = '\033[0m'
#     BGRED       = '\u001b[41;1m'
#     BGGREEN     = '\u001b[42;1m'
#     BGBLUE      = '\u001b[44;1m'
#     BGYELLOW    = '\u001b[43;1m'
#     BRRED       = '\u001b[31;1m'
#     BRGREEN     = '\u001b[32;1m'
#     BRLBLUE     = '\u001b[36;1m'
#     BRDBLUE     = '\u001b[34;1m'
#     BRYELLOW    = '\u001b[33;1m'
#     BRMAROON    = '\u001b[35;1m'
#     BRPURPLE    = '\u001b[30;1m'
#     CGRAY       = '\u001b[38;5;240m'
#     CWHITE      = '\u001b[38;5;255m'

# #endregion



# #region DEFINITIONS

# def remove_duplicates(seq):
#     seen = set()
#     seen_add = seen.add
#     return [x for x in seq if not (x in seen or seen_add(x))]

# # def find_songs(analysis_type, album_uri):
    
# #     album_name = sp.album(album_uri)["name"]
# #     artist_name = sp.album(album_uri)["artists"][0]["name"]
    
# #     if (analysis_type == "Bangers"):
        
# #         playlist = banger_playlist
        
# #         sys.stdout.flush()
# #         sys.stdout.write(f"\nFinding {TerminalColors.BRDBLUE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
    
# #     elif (analysis_type == "Chill Hits"):
        
# #         playlist = chill_playlist
        
# #         sys.stdout.flush()
# #         sys.stdout.write(f"\nFinding {TerminalColors.BRPURPLE}{analysis_type}{TerminalColors.ENDC} on {TerminalColors.BRMAROON}\"{album_name}\"{TerminalColors.ENDC} by {TerminalColors.BRYELLOW}{artist_name}{TerminalColors.ENDC}... ")
        
# #     else:
# #         playlist = None
        
# #     # declare attribute lists
# #     track_uri = []
# #     saved_track_uri = []
# #     popularity = []
# #     sorted_popularity = []
# #     low_loudness = []
# #     high_loudness = []
# #     loudness = [low_loudness, high_loudness]
# #     calculate_loudness_mean = []
# #     calculate_danceability_mean = []
# #     calculate_acousticness_mean = []
# #     loudness_mean = []
# #     danceability_mean = []
# #     acousticness_mean = []
# #     attributes = ["danceability", "acousticness"]
# #     calculate_all_means = [calculate_danceability_mean, calculate_acousticness_mean]
# #     means = [danceability_mean, acousticness_mean]

# #     # get interested album
# #     tracks = sp.album_tracks(album_uri)
        
# #     # get track uri from album
# #     for c in tracks["items"]:
# #         if c["duration_ms"] >= 60000 and "intro" not in c["name"].lower() and "outro" not in c["name"].lower() and "skit" not in c["name"].lower() and "speaks" not in c["name"].lower():
# #             track_uri.append(c["uri"])
        
# #     # determine loudness mean
# #     for d in track_uri:
# #         features = sp.audio_features(tracks=[d])
# #         calculate_loudness_mean.append(features[0]["loudness"])
# #     loudness_mean.append(statistics.mean(calculate_loudness_mean))
    
# #     # sort tracks based on loudness
# #     for e in track_uri:
# #         features = sp.audio_features(tracks=[e])
# #         if features[0]["loudness"] < loudness_mean[0]:
# #             low_loudness.append(e)
# #         else:
# #             high_loudness.append(e)
    
# #     # calculate danceability and acousticness means
# #     for f in loudness:
# #         for g, h, i in zip(attributes, calculate_all_means, means):
# #             for j in f:
# #                 features = sp.audio_features(tracks=[j])
# #                 h.append(features[0][g])
# #             i.append(statistics.mean(h))
# #             h.clear()
    
# #     if (analysis_type == 'Bangers'):
# #         # determine potential bangers
# #         for k, l, m in zip(loudness, danceability_mean, acousticness_mean):
# #             for n in k:
# #                 features = sp.audio_features(tracks=[n])
# #                 track = sp.track(n)
# #                 if features[0]["danceability"] >= l and features[0]["acousticness"] <= m:
# #                     saved_track_uri.append(n)
# #                 if track["album"]["release_date"] >= date.today().strftime("%Y-%m-%d"):
# #                     continue
# #                 else:
# #                     popularity.append((features[0]["uri"], track["popularity"]))
                    
# #     if (analysis_type == 'Chill Hits'):
# #         # determine potential bangers
# #         for k, l, m in zip(loudness, danceability_mean, acousticness_mean):
# #             for n in k:
# #                 features = sp.audio_features(tracks=[n])
# #                 track = sp.track(n)
# #                 if features[0]["danceability"] <= l and features[0]["acousticness"] >= m:
# #                     saved_track_uri.append(n)
# #                 if track["album"]["release_date"] >= date.today().strftime("%Y-%m-%d"):
# #                     continue
# #                 else:
# #                     popularity.append((features[0]["uri"], track["popularity"]))
    
# #     # sort songs by popularity
# #     if len(popularity) > 0:
# #         sorted_popularity = sorted(popularity, key=lambda x: x[1], reverse=True)
    
# #     if (analysis_type == 'Bangers') and (len(sorted_popularity) > 0):
# #         saved_track_uri.append(sorted_popularity[0][0])
# #         saved_track_uri = remove_duplicates(saved_track_uri)
        
# #     if (analysis_type == 'Chill Hits') and (len(sorted_popularity) > 0):
# #         most_popular = sorted_popularity[0][0]
# #         if most_popular in saved_track_uri:
# #             saved_track_uri.remove(most_popular)
    
# #     # print track names to terminal
# #     if len(saved_track_uri) == 0:
# #         sys.stdout.write(f"{TerminalColors.BRRED}Found 0 Songs!{TerminalColors.ENDC}")
# #     elif len(saved_track_uri) == 1:
# #         sys.stdout.write(f"{TerminalColors.BRGREEN}Found {len(saved_track_uri)} Song!{TerminalColors.ENDC}")
# #     else:
# #         sys.stdout.write(f"{TerminalColors.BRGREEN}Found {len(saved_track_uri)} Songs!{TerminalColors.ENDC}")
        
# #     sys.stdout.flush()
# #     print('\n')
# #     for (o, p) in enumerate(saved_track_uri, start=1):
# #         features = sp.audio_features(tracks=[p])
# #         track = sp.track(p)
# #         print(str(o) + ". " + track["name"])

# #     # save tracks to playlist
# #     #sp.playlist_add_items(playlist, saved_track_uri)

# #endregion



# #region LOGIC

# # # error handling for command line arguments
# # if (len(args.album_uri) != 36 and len(args.album_uri) != 39) or (args.album_uri[0:14] != "spotify:album:" and args.album_uri[0:17] != "spotify:playlist:"):
# #     print(f"\n{TerminalColors.BRRED}Not a valid URI. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
# #     exit()

# # # album analysis preprocessing
# # if args.album_uri[0:14] == "spotify:album:":
# #     tracks = sp.album_tracks(args.album_uri)
# #     if tracks["total"] <= 2:
# #         print(f"\n{TerminalColors.BRRED}Need more songs to analyze. Retry with an appropriate album or playlist URI.{TerminalColors.ENDC}")
# #         exit()
# #     else:
# #         all_album_uri = [args.album_uri]
    
# # # playlist analysis preprocessing
# # if args.album_uri[0:17] == "spotify:playlist:":
# #     all_album_uri = []
# #     all_albums = sp.playlist_items(args.album_uri)
# #     for i in range(len(all_albums["items"])):
# #         if all_albums["items"][i]["track"]["album"]["album_type"] == 'single' and all_albums["items"][i]["track"]["album"]["total_tracks"] > 2:
# #             continue
# #         else:
# #             all_album_uri.append(all_albums["items"][i]["track"]["album"]["uri"])
# #         # code for analyzing a playlist for bangers and chill hits
# #         #print(all_albums["items"][i]["track"]["uri"])
# #         #all_album_uri.append(all_albums["items"][i]["track"]["uri"])
# #     all_album_uri = remove_duplicates(all_album_uri)

# # # driver code
# # for album_uri in all_album_uri:
# #     find_songs("Bangers", album_uri)
# #     find_songs("Chill Hits", album_uri)

# #endregion



# #region UNUSED CODE

# all_album_uri = []
# playlist = 'spotify:playlist:7hJacr1uy6B5E1gQKQOyFG'

# # get list of albums
# all_albums = sp.playlist_items('spotify:playlist:0fJPai6RFrgFPoTSYBUSuk')
# for i in range(len(all_albums["items"])):
#     all_album_uri.append(all_albums["items"][i]["track"]["uri"])
# all_album_uri = remove_duplicates(all_album_uri)

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
# calculate_all_means = [calculate_danceability_mean, calculate_acousticness_mean]
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
#     for g, h, m in zip(attributes, calculate_all_means, means):
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

# # print track names
# for i in saved_uri:
#     features = sp.audio_features(tracks=[i])
#     track = sp.track(i)
#     print(track["name"])

# # save tracks to playlist
# sp.playlist_add_items(playlist, saved_uri)

# # print success message
# print('--------------------')
# print('Success!')

# #endregion
