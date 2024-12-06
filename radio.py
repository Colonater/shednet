from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from pytube import Search, YouTube
from pydub import AudioSegment
import os
import urllib.error

radio_bp = Blueprint('radio', __name__, url_prefix='/radio')

# Ensure the music directory exists
if not os.path.exists('static/music'):
    os.makedirs('static/music')

latest_song = None

@radio_bp.route('/')
def radio():
    # List all songs in the static/music directory and render the radio page
    songs = os.listdir('static/music')
    return render_template('radio.html', songs=songs, latest_song=latest_song)

@radio_bp.route('/search', methods=['POST'])
def search():
    # Search for a song on YouTube by name, download it, and convert it to MP3
    song_name = request.form['song_name']
    search = Search(song_name)
    results = search.results
    if results:
        video = results[0]
        video_url = video.watch_url
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True).first()
            output_file = stream.download(output_path='static/music')
            base, ext = os.path.splitext(output_file)
            mp3_file = base + '.mp3'
            AudioSegment.from_file(output_file).export(mp3_file, format='mp3')
            os.remove(output_file)  # Remove the original file
            global latest_song
            latest_song = os.path.basename(mp3_file)
            return redirect(url_for('radio.radio'))
        except urllib.error.HTTPError as e:
            return f"HTTP Error: {e.code} - {e.reason}", 403
    else:
        return "No results found", 404

@radio_bp.route('/music/<filename>')
def play(filename):
    # Serve the MP3 files from the static/music directory
    return send_from_directory('static/music', filename)