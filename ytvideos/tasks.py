from ytfetch.celery import app
from googleapiclient.discovery import build
from ytfetch import settings
import datetime
from ytvideos.models import Video

@app.task
def get_videos_from_youtube_api_and_store():
    query = 'news'

    # calculate the publishedAfter datetime as current datetime minus 10 seconds
    published_after_datetime = datetime.datetime.now() - datetime.timedelta(seconds=30)
    published_after = published_after_datetime.isoformat()  # Convert to ISO format

    # service object for the YouTube Data API
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    
    # send request to the YouTube Data API to search for videos based on the query
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        order='date',
        publishedAfter=published_after+'Z',
    ).execute()
    print(search_response)

    # extract the video items from the API response
    videos = search_response.get('items', [])
    
    # store the video data into db
    for video in videos:
        Video.objects.create(title=video["snippet"]["title"], description=video["snippet"]["description"], publishing_datetime=video["snippet"]["publishedAt"], thumbnail_url=video["snippet"]["thumbnails"]["default"]["url"], video_id=video["id"]["videoId"])
        print(video)