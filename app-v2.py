import os
from flask import Flask, render_template, request, send_file, abort
from yt_dlp import YoutubeDL

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    fmt = request.form.get('format', 'video')  # 'video', 'audio', atau 'both'
    if not url:
        abort(400, description="URL tidak boleh kosong")

    # Konfigurasi yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if fmt == 'audio'
                  else 'bestvideo+bestaudio/best',
        # merge output jadi mp4
        'merge_output_format': 'mp4',
        # opsi untuk memaksa re-encode video ke H.264 dan audio ke AAC
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedcodec': 'h264',      # AVC/H.264
            },
            {
                'key': 'FFmpegAudioConvertor',
                'preferedcodec': 'aac',       # AAC
            }
        ],
        # tambahan argumen ke ffmpeg (opsional, tapi bisa memperkuat kontrol)
        'postprocessor_args': [
            '-c:v', 'libx264',
            '-c:a', 'aac',
            # contohnya untuk kualitas video/crf:
            '-crf', '23',   # crf 18–28, makin kecil makin tajam+besar
            '-preset', 'medium'
        ],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # yt-dlp biasanya menambahkan ekstensi .mp4 setelah konversi
            filename = os.path.splitext(filename)[0] + '.mp4'
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Terjadi kesalahan: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5342)
