import asyncio
import re

import dataset
import httpx

from bs4 import BeautifulSoup
from dynaconf import settings


async def search_from_api(track: dict, client) -> dict:
    response = await client.get(
        "https://www.googleapis.com/youtube/v3/search",
        params={
            "key": settings.YOUTUBE_API_KEY,
            "part": "id,snippet",
            "order": "relevance",
            "q": track["title"],
            "type": "video",
        },
        timeout=None,
    )
    assert response.status_code == 200, response.json()["error"]["message"]
    data = response.json()
    track.update(
        {
            "youtube_results": [
                {
                    "title": item["snippet"]["title"],
                    "url": "https://www.youtube.com/watch?v=" + item["id"]["videoId"],
                    "video_id": item["id"]["videoId"],
                    "track_id": track["id"],
                    "downloaded": False,
                }
                for item in data["items"]
            ]
        }
    )
    return track


async def search_from_site(track: dict, client) -> dict:
    result = await client.get(
        f"https://www.youtube.com/results?search_query={track['title']}", timeout=20
    )
    assert result.status_code == 200

    # Parse
    soup = BeautifulSoup(result.content, "html.parser")
    pattern = re.compile(r"/watch\?v=")
    found = soup.find_all("a", "yt-uix-tile-link", href=pattern)

    track.update(
        {
            "searched": True,
            "youtube_results": [
                {
                    "title": x.text,
                    "url": "https://www.youtube.com" + x.get("href", ""),
                    "video_id": x.get("href", "").replace("/watch?v=", ""),
                    "track_id": track["id"],
                    "downloaded": False,
                }
                for x in found
                if "list" not in x.get("href", "")
            ]
        }
    )
    return track


async def search(track: dict, client) -> dict:
    try:
        return await search_from_api(track, client)
    except AssertionError:
        return await search_from_site(track, client)


def list_tracks(db):
    query = (
        "SELECT "
        "t.id, t.title || ' - ' || a.name AS title, t.downloaded "
        "FROM tracks t "
        "INNER JOIN artists a ON t.artist_id = a.id "
        "WHERE t.searched IS NOT TRUE "
    )
    return db.query(query)


def persist_results(db, tracks):
    for track in tracks:
        db["tracks"].update({"id": track["id"], "searched": True}, ["id"])
        for item in track["youtube_results"][:5]:
            db["youtube_results"].insert_ignore(item, ["video_id", "track_id"])


async def main(db):
    """
    Searches for tracks on youtube and stores the results in database
    :param db:
    :return:
    """
    tracks = list(list_tracks(db))
    step = 50
    async with httpx.AsyncClient() as client:
        for i in range(0, len(tracks), step):
            result = await asyncio.gather(
                *(search_from_site(track, client) for track in tracks[i : i + step])
            )
            persist_results(db, result)


if __name__ == "__main__":
    db = dataset.connect(settings.DATABASE_URI)
    asyncio.run(main(db))
