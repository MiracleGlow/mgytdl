import os
from flask import Flask, render_template, request, send_file, abort
from yt_dlp import YoutubeDL

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    # Halaman form input URL dan format
    return render_template('index.html')
    # Kita menggunakan route decorator dari Flask :contentReference[oaicite:2]{index=2}

@app.route('/download', methods=['POST'])
def download():
    url    = request.form.get('url')
    fmt    = request.form.get('format', 'video')  # 'video', 'audio', atau 'both'
    if not url:
        abort(400, description="URL tidak boleh kosong")

    # Konfigurasi yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # template nama file :contentReference[oaicite:3]{index=3}
        'format': 'bestaudio/best' if fmt == 'audio'
                  else 'bestvideo+bestaudio/best',                     # pilihan format stream :contentReference[oaicite:4]{index=4}
        'merge_output_format': 'mp4',                                  # gabungkan video+audio ke MP4 :contentReference[oaicite:5]{index=5}
    }

    try:
        # Unduh dengan yt-dlp sebagai library 
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        # Kirim file ke user sebagai attachment :contentReference[oaicite:7]{index=7}
        return send_file(filename, as_attachment=True)
    except Exception as e:
        # Tampilkan pesan kesalahan sederhana
        return f"Terjadi kesalahan: {e}", 500

if __name__ == '__main__':
    # Jalankan server debug mode untuk pengembangan :contentReference[oaicite:8]{index=8}
    app.run(host='0.0.0.0', port=5342)
