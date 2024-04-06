from ytfetch.celery import app
from googleapiclient.discovery import build
from ytfetch import settings
import datetime
from ytvideos.models import Video
from googleapiclient.errors import HttpError

@app.task
def get_videos_from_youtube_api_and_store(query='news'):
    # calculate the publishedAfter datetime as current datetime minus 10 seconds
    published_after_datetime = datetime.datetime.now() - datetime.timedelta(seconds=10)
    published_after = published_after_datetime.isoformat()  # Convert to ISO format

    for api_key in settings.YOUTUBE_API_KEYS:
        try:
            # service object for the YouTube Data API
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # send request to the YouTube Data API to search for videos based on the query
            search_response = youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                order='date',
                publishedAfter=published_after+'Z',
                maxResults=50,
            ).execute()
            print(search_response)

            # extract the video items from the API response
            videos = search_response.get('items', [])
            
            # store the video data into db
            for video in videos:
                try:
                    Video.objects.create(title=video["snippet"]["title"], description=video["snippet"]["description"], publishing_datetime=video["snippet"]["publishedAt"], thumbnail_url=video["snippet"]["thumbnails"]["default"]["url"], video_id=video["id"]["videoId"])
                except Exception as error:
                    print(error)
                print(video)
            
            # return if video data found from given api key
            return
        except HttpError as e:
            if e.resp.status == 403:  # quota exceeded error
                print("Quota exhausted for this API key trying api call with next one")
                continue  # try the next API key
            else:
                raise  