import yt_dlp
from typing import List, Optional

from structs import YoutubeVideo, log


def search_yt(query: str, max_results: int = 5) -> List[YoutubeVideo]:
    """
    Search YouTube for a query and return video info.

    :param query: Search string for YouTube.
    :param max_results: Number of results to return.
    :return: List of dicts containing video metadata.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # Don't resolve full playlist items
    }
    
    search_query = f"ytsearch{max_results}:{query}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(search_query, download=False)
        return [ YoutubeVideo(
            id=json_data['id'],
            url=json_data['url'],
            title=json_data['title'],
            description=json_data.get('description'),
            duration=int(json_data.get('duration', 0)),
            thumbnails=[thumb["url"] for thumb in json_data.get('thumbnails')],
            views=json_data.get('view_count')
        ) for json_data in info.get('entries', [])]

# Example usage
if __name__ == "__main__":
    results = search_yt("lofi hip hop")
    for idx, video in enumerate(results, start=1):
        log(idx, video)
