from django.shortcuts import render
from django.http import JsonResponse
from .serializers import PostSerializer
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .forms import PostForm
from account.serializers import UserSerializer
from account.models import User,FriendshipRequest
from django.db.models import Q
from itertools import chain


@api_view(['GET'])
def post_list(request):
    user = User.objects.get(id=request.user.id)
    user_friends_list = [user.id] + [x for x in user.friends.all()] 
    posts = Post.objects.filter(created_by_id__in=user_friends_list)
    serializer = PostSerializer(posts,many=True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
def post_list_profile(request,id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(created_by__id=id)

    user_serializer = UserSerializer(user)
    post_serializer = PostSerializer(posts,many=True)

    existing_request = FriendshipRequest.objects.filter(
        (Q(created_for=user, created_by=request.user) | Q(created_for=request.user, created_by=user)),
        status='sent'
    )

    friends = user.friends.filter(id=request.user.id).exists()


    if existing_request:
        return JsonResponse({
                'posts':post_serializer.data,
                'user':user_serializer.data,
                'existing_request':True,
                'friends':friends},
                safe=False)
    else:
        return JsonResponse({
            'posts':post_serializer.data,
            'user':user_serializer.data,
            'existing_request':False,
            'friends':friends},
            safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)
        return JsonResponse(serializer.data,safe=False)
    else:
        return JsonResponse({'hello':'herp'})




