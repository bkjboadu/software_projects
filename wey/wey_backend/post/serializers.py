from .models import Post
from rest_framework import serializers
from account.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id','body','likes_count','created_at_formatted','created_by')