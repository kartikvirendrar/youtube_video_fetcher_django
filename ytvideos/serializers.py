from rest_framework import serializers
from ytvideos.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'publishing_datetime', 'thumbnail_url', 'video_id']
