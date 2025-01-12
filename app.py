import subprocess
# Helper functions
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

