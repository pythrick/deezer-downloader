import httpx
import dataset

from dynaconf import settings


def main(db):
    """
    Consumes Deezer API and get list of my favorite tracks and stores in database
    :param db:
    :return:
    """
    url = f"https://api.deezer.com/user/me/tracks?output=json&access_token={settings.DEEZER_ACCESS_TOKEN}"
    while url:
        result = httpx.get(url)
        assert result.status_code == 200
        content = result.json()
        for track in content["data"]:
            artist = track.pop("artist")
            db["artists"].insert_ignore(artist, ["id"])
            album = track.pop("album")
            db["albums"].insert_ignore(album, ["id"])
            track["artist_id"] = artist["id"]
            track["album_id"] = album["id"]
            db["tracks"].insert_ignore(track, ["id"])
        url = content.get("next")


if __name__ == "__main__":
    db = dataset.connect(settings.DATABASE_URI)
    main(db)
