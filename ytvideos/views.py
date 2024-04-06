from rest_framework import viewsets, pagination
from .models import Video
from .serializers import VideoSerializer
from rest_framework.response import Response

class VideoPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.order_by('-publishing_datetime')
    serializer_class = VideoSerializer
    pagination_class = VideoPagination
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    