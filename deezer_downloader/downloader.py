import logging
import os
import dataset

from dynaconf import settings
from youtube_dl import YoutubeDL


def download(db, track: dict):
    print("Downloading: ", track["title"])
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "256",
            }
        ],
        "logger": logging.getLogger("youtube_dl"),
        "outtmpl": os.path.join(settings.DESTINATION_DIR, "%(title)s.%(ext)s"),
    }
    try:
        # Download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([track["url"]])

        # Mark track as downloaded
        db["tracks"].update({"id": track["id"], "downloaded": True}, ["id"])
        db["youtube_results"].update({"id": track["yt_res_id"], "downloaded": True}, ["id"])
        print("Downloaded: ", track["title"])
    except Exception as e:
        print("Unable to download: ", track["title"], e)


def list_tracks(db):
    query = (
        "SELECT "
        "t.id, y.title, y.url, y.video_id, MIN(y.id) AS yt_res_id "
        "FROM youtube_results y "
        "INNER JOIN tracks t ON t.id = y.track_id "
        "INNER JOIN artists a ON t.artist_id = a.id "
        "WHERE t.downloaded IS NOT TRUE "
        "GROUP BY y.track_id "
    )
    return db.query(query)


def main(db):
    """
    Downloads tracks from Youtube in mp3 format
    :param db:
    :return:
    """
    for track in list_tracks(db):
        download(db, track)


if __name__ == "__main__":
    db = dataset.connect(settings.DATABASE_URI)
    main(db)
