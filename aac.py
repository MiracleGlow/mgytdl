import os
import subprocess
import yt_dlp
import gradio as gr

# Pastikan ffmpeg ada di PATH, atau tulis path lengkapnya
FFMPEG_PATH = "ffmpeg"  # ganti jika ffmpeg tidak di PATH

def download_youtube_audio(url):
    try:
        # Folder output
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)

        # Download audio terbaik dalam format m4a
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            input_file = ydl.prepare_filename(info)

        # Nama file output AAC 128kbps
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + ".mp3"

        # Konversi ke mp3 AAC 128kbps
        cmd = [
            FFMPEG_PATH,
            "-y",  # overwrite
            "-i", input_file,
            "-vn",
            "-c:a", "aac",
            "-b:a", "128k",
            output_file
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Hapus file asli setelah konversi
        if os.path.exists(input_file):
            os.remove(input_file)

        return output_file
    except Exception as e:
        return f"Error: {e}"

def gradio_app(url):
    file_path = download_youtube_audio(url)
    if os.path.isfile(file_path):
        return file_path
    else:
        return None

# UI Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🎵 YouTube to AAC 128kbps MP3 Downloader")
    url_input = gr.Textbox(label="YouTube URL", placeholder="Masukkan link YouTube...")
    output_audio = gr.File(label="Hasil Download (MP3)")
    download_btn = gr.Button("Download")

    download_btn.click(fn=gradio_app, inputs=url_input, outputs=output_audio)

if __name__ == "__main__":
    demo.launch()
