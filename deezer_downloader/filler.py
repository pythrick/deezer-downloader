import os
import re
import time

from random import randint
from typing import Optional

import dataset
import eyed3
import httpx

from bs4 import BeautifulSoup
from dynaconf import settings


def list_tracks(db):
    query = (
        "SELECT "
        "t.id, t.title, a.name as artist, b.title as album, b.cover_big as cover, y.title  || '.mp3' as file, y.id AS yt_id "
        "FROM youtube_results y "
        "INNER JOIN tracks t ON t.id = y.track_id "
        "INNER JOIN artists a ON t.artist_id = a.id "
        "INNER JOIN albums b ON t.album_id = b.id "
        "WHERE y.downloaded IS TRUE "
        "AND t.filled IS NOT TRUE "
    )
    tracks_map = get_tracks_map()
    return [t for t in db.query(query) if hash_string(t["file"]) in tracks_map]


def get_album_cover(track: dict) -> Optional[bytes]:
    response = httpx.get(track["cover"], timeout=10)
    assert response.status_code == 200, (
        "Unable to get album cover to: " + track["title"]
    )
    return response.content


def get_lyrics(track: dict) -> Optional[str]:
    artist = track["artist"].lower()
    title = track["title"].lower()

    query = f"{artist} {title}".replace(" ", "+")

    url = f"https://search.azlyrics.com/search.php?q={query}"
    response = httpx.get(url)
    assert response.status_code == 200, (
        "Unable to search lyrics to: " + track["title"]
    )

    soup = BeautifulSoup(response.content, "html.parser")
    found = soup.find_all("td", "text-left")
    url = next(
        (
            x.contents[1]["href"]
            for x in found
            if title in found[0].contents[1].text.lower()
            and artist in x.contents[3].text.lower()
        ),
        None,
    )

    if not url:
        return None

    # Lyrics - Detail Page
    response = httpx.get(url)
    assert response.status_code == 200, (
            "Unable to search lyrics to: " + track["title"]
    )
    soup = BeautifulSoup(response.content, "html.parser")
    lyrics = str(soup)
    # lyrics lies between up_partition and down_partition
    up_partition = "<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->"
    down_partition = "<!-- MxM banner -->"
    lyrics = lyrics.split(up_partition)[1]
    lyrics = lyrics.split(down_partition)[0]

    lyrics = BeautifulSoup(lyrics, "html.parser").text.strip()
    return lyrics


def hash_string(s):
    pattern = re.compile("[\W_]+")
    return pattern.sub("", s.lower())


def get_tracks_map():
    tracks_map = {}
    for track in os.listdir(settings.DESTINATION_DIR):
        tracks_map[hash_string(track)] = track

    return tracks_map


def fill_info(track: dict):
    tracks_map = get_tracks_map()
    file_name = tracks_map.get(hash_string(track["file"]))
    if not file_name:
        return
    audiofile = eyed3.load(os.path.join(settings.DESTINATION_DIR, file_name))
    audiofile.tag.artist = track["artist"]
    audiofile.tag.album = track["album"]
    audiofile.tag.title = track["title"]

    try:
        album_cover = get_album_cover(track)
        if album_cover:
            audiofile.tag.images.set(0, album_cover, "image/jpeg", "Album Art")
    except Exception as e:
        print(e)
    try:
        lyrics = get_lyrics(track)
        if lyrics:
            audiofile.tag.lyrics.set(lyrics)
    except Exception as e:
        print(e)

    audiofile.tag.save()


def persist_track_info(db, track):
    db["tracks"].update({"id": track["id"], "filled": True, "downloaded": True}, ["id"])


def main(db):
    """
    Fills the id3 tags inside tracks
    :param db:
    :return:
    """
    tracks = list_tracks(db)
    tracks_amount = len(tracks)
    for i, track in enumerate(tracks):
        try:
            fill_info(track)
            persist_track_info(db, track)
        except Exception as e:
            print(e)

        print("Track filled: ", track["title"], f"{i+1}/{tracks_amount}")
        time.sleep(randint(5, 20) / 10)


if __name__ == "__main__":
    db = dataset.connect(settings.DATABASE_URI)
    main(db)
