from flask import send_file, Flask, request, jsonify, render_template
import yt_dlp
import os
import re

app = Flask(__name__)

OUTPUT_DIR = r"C:\Users\smrit\Documents\Sim\Repo\youtubetomp3"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_filename(name):
    name = re.sub(r'[^\w\-_\. ]', '_', name)
    return name

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    url = data.get("url")

    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            raw_filename = ydl.prepare_filename(info)
            filename = clean_filename(os.path.basename(raw_filename))
            safe_path = os.path.join(OUTPUT_DIR, filename)
            os.rename(raw_filename, safe_path)
            print("Trying to send:", safe_path)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

    filename = os.path.basename(filename)

    return jsonify(
        success=True,
        filename=filename,
        download_url=f"https://youtubeutility-production.up.railway.app/download/{filename}"
    )


    @app.route("/download/<path:filename>", methods=["GET"])
    def download(filename):
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify(success=False, error="File not found"), 404

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=8080)


