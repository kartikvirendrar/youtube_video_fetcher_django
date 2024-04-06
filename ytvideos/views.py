from rest_framework import viewsets, pagination
from .models import Video
from .serializers import VideoSerializer
from rest_framework.response import Response
from django.shortcuts import render

class VideoPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset to retrieve Video objects ordered by publishing_datetime in descending order
    queryset = Video.objects.order_by('-publishing_datetime')
    # serializer class to serialize Video objects
    serializer_class = VideoSerializer
    # pagination class to paginate the queryset
    pagination_class = VideoPagination
    
    def list(self, request, *args, **kwargs):
        # get the queryset after applying filters
        queryset = self.filter_queryset(self.get_queryset())
        # paginate the queryset
        page = self.paginate_queryset(queryset)

        # serialize and return paginated response
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
def video_dashboard(request):
    videos = Video.objects.all()

    # apply filters based on user input, more fields can be added to filter from
    title_filter = request.GET.get('title')
    if title_filter:
        videos = videos.filter(title__icontains=title_filter)

    # apply sorting based on user input, more fields can be added to sort from
    sort_by = request.GET.get('sort_by', 'publishing_datetime')
    if sort_by == 'publishing_datetime':
        videos = videos.order_by('-publishing_datetime')
    elif sort_by == 'title':
        videos = videos.order_by('title')

    context = {
        'videos': videos,
    }

    return render(request, 'dashboard.html', context)
    