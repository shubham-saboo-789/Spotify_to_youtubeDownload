# import os
# import yt_dlp
# from flask import Flask, request, send_file, render_template

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# from youtubesearchpython import VideosSearch


# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')


# def get_playlist_tracks_from_url(playlist_url):
#     # Set up your Spotify credentials
#     client_id = 'da6b139e19754cbcb15f6ce202f54746'
#     client_secret = '3d00001e4ba14ba68c9a0c7c9af332e3'

#     # Authenticate
#     auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#     sp = spotipy.Spotify(auth_manager=auth_manager)

#     # Extract playlist ID from URL
#     playlist_id = playlist_url.split('/')[-1].split('?')[0]

#     # Fetch playlist tracks
#     results = sp.playlist_tracks(playlist_id)
#     tracks = results['items']
#     while results['next']:
#         results = sp.next(results)
#         tracks.extend(results['items'])
    
#     # Get track names
#     track_names = [track['track']['name'] for track in tracks]
#     return track_names


# def search_youtube(song_name):
#     # Search for the song on YouTube
#     videos_search = VideosSearch(song_name, limit=1)
    
#     # Get the first video from the search results
#     result = videos_search.result()['result'][0]
    
#     # Extract the video link
#     video_link = result['link']
    
#     return video_link


# def download_audio(youtube_url):
#     # youtube_url = request.form['youtube_url']
#     try:
#         # Get the user's Downloads directory
#         user_profile = os.environ.get('USERPROFILE')
#         downloads_dir = os.path.join(user_profile, 'Downloads')

#         # Path to the ffmpeg executable (can be used when ffmpeg is in the same directory as app.py)
#         # ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'bin')

#         # Set the output template for saving the file
#         output_path = os.path.join(downloads_dir, '%(title)s.%(ext)s')  # Save with video title as filename in the 'Downloads' folder

#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': output_path,  # Use the video title for filename in the specified folder  
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
#                 'preferredcodec': 'mp3',     # Save the file as .mp3
#                 'preferredquality': '192',    # Audio quality
#             }],
#             'ffmpeg_location': 'C:/ffmpeg/bin',  # specify the path to ffmpeg
#             'noplaylist': True,  # Ensure only the single video is downloaded, not playlists
#             'quiet': True,  # Suppress output from yt-dlp
#             'progress_hooks': [lambda d: None],  # Suppress progress messages
#         }
#             # 'ffmpeg_location': 'C:\ffmpeg\bin',  # absolute path to ffmpeg

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(youtube_url, download=True)
#             filename = os.path.join(downloads_dir, f"{info['title']}.mp3")

#         # Check if the file exists and send it for download
#         if os.path.exists(filename):
#             return send_file(filename, as_attachment=True, download_name=f"{info['title']}.mp3")

#         return "Error: Audio file not found."

#     except Exception as e:
#         return f"Error: {str(e)}"


# @app.route('/convert', methods=['POST'])
# def convert():
#     playlist_link = request.form['playlist_link']
#     print(playlist_link)
    
#     song_list = get_playlist_tracks_from_url(playlist_link)
#     print(song_list)
#     # under testing
#     for song in song_list:
#         print(f"Downloading: {song}")
#         youtube_link=search_youtube(song)
#         print(youtube_link)
#         download_audio(youtube_link)
        
#     return f"downloading : {song_list} "

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import yt_dlp
from flask import Flask, request, send_file, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def get_playlist_tracks_from_url(playlist_url):
    client_id = 'da6b139e19754cbcb15f6ce202f54746'
    client_secret = '3d00001e4ba14ba68c9a0c7c9af332e3'

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    track_names = [track['track']['name'] for track in tracks]
    return track_names


def search_youtube(song_name):
    videos_search = VideosSearch(song_name, limit=1)
    result = videos_search.result()['result'][0]
    return result['link']


def download_audio(youtube_url):
    try:
        user_profile = os.environ.get('USERPROFILE')
        downloads_dir = os.path.join(user_profile, 'Downloads')
        output_path = os.path.join(downloads_dir, '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': 'C:/ffmpeg/bin',
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            filename = os.path.join(downloads_dir, f"{info['title']}.mp3")

        if os.path.exists(filename):
            return send_file(filename, as_attachment=True, download_name=f"{info['title']}.mp3")
        return "Error: Audio file not found."

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/convert', methods=['POST'])
def convert():
    playlist_link = request.form['playlist_link']
    song_list = get_playlist_tracks_from_url(playlist_link)
    
    for song in song_list:
        youtube_link = search_youtube(song)
        download_audio(youtube_link)
        
    return f"Downloading: {song_list}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False )


# playlist_url = 'https://open.spotify.com/playlist/4jrqpB0oAqwHXezHhZThgH?si=ca72d0d4394945a6'