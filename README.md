Django Command-

    python ytfetch/manage.py runserver

Celery Commands-

    celery -A ytfetch worker --loglevel=info
    celery -A ytfetch beat -l info

API's-

    GET /api/videos: 
        endpoint to retrieve a list of videos with pagination.

        Query Parameters:
            - page: page number to retrieve. Default: 1.
            - page_size: expected number of videos per page. Default: 10.

        Example Response:
        paginated list of video objects with the following fields-
            {
                "count": 100,
                "next": "http://example.com/api/videos/?page=2&page_size=10",
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "title": "Sample Video",
                        "description": "This is a sample video.",
                        "published_at": "2024-04-06T12:00:00Z",
                        "thumbnail_url": "http://youtube.com/thumbnail.png"
                    },
                    ...
                ]
            }

        Example Request:
            GET /api/videos/?page=1&page_size=10

Dashboard-

    Video Dashboard: http://localhost:8000/dashboard