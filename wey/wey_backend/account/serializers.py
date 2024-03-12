from rest_framework import serializers
from .models import User,FriendshipRequest

class UserSerializer(serializers.ModelSerializer):
    friends_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','name','email','friends_count')

    def get_friends_count(self, obj):
        return getattr(obj,'friends_count',obj.friends.count())


class FriendRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FriendshipRequest
        fields = ('id','created_by')
