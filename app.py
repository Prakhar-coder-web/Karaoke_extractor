from flask import Flask, flash, redirect, render_template, request, send_file, url_for
import subprocess
import os
import shutil
import threading
import time

app = Flask(__name__)
app.secret_key = 'shaw245hd39dj'
AUDIO_DIR = 'static/audio'
SEPARATED_DIR = os.path.join(AUDIO_DIR, 'separated')


def extract_audio(youtube_url, output_audio_path):
    command = [
        'yt-dlp',
        '-x', '--audio-format', 'mp3',
        '-o', output_audio_path,
        youtube_url
    ]
    subprocess.run(command, check=True)


def separate_audio(input_file, output_dir):
    command = [
        'demucs',
        '--name', 'htdemucs',
        '--two-stems', 'vocals',
        '--out', output_dir,
        input_file
    ]
    subprocess.run(command, check=True)


def delete_files_after_delay(audio_file, folder_path, delay=120):
    time.sleep(delay)
    if os.path.exists(audio_file):
        os.remove(audio_file)
        print(f"Deleted file: {audio_file}")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")


@app.route('/process', methods=['POST'])
def process():
    youtube_url = request.form['youtube_url']
    try:
        output_audio_path = os.path.join(AUDIO_DIR, 'output.mp3')
        extract_audio(youtube_url, output_audio_path)

        separate_audio(output_audio_path, SEPARATED_DIR)

        vocals_file = 'audio/separated/htdemucs/output/vocals.wav'
        karaoke_file = 'audio/separated/htdemucs/output/no_vocals.wav'

        flash('Audio processed successfully! Vocals and karaoke files are available.', 'success')

        threading.Thread(target=delete_files_after_delay, args=(
            output_audio_path, SEPARATED_DIR)).start()

        return render_template('index.html', vocals_file=vocals_file, karaoke_file=karaoke_file)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download/<path:filename>')
def download(filename):
    file_path = os.path.join(
        'static', 'audio', 'separated/htdemucs/output', filename)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
