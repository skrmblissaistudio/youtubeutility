from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__)

OUTPUT_DIR = r"C:\Users\smrit\Documents\Sim\Repo\youtubetomp3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return jsonify(success=True, filename=filename)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=8080)

