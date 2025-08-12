import os
from flask import Flask, render_template, request, send_file, abort
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Folder untuk menyimpan hasil unduhan
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    ext = request.form.get('ext')  # 'mp4', 'webm', atau 'mkv'
    if not url or not ext:
        abort(400, description="URL dan format harus dipilih")

    # Opsi yt-dlp: ambil best muxed format dengan ekstensi yang dipilih
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': f'best[ext={ext}]',  # langsung file muxed asli
        # hilangkan pengaturan merge_output_format & ffmpeg
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Terjadi kesalahan saat mengunduh: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
