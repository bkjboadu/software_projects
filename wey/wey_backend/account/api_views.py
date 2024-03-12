from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from .models import User,FriendshipRequest
from .forms import SignupForm
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer,FriendRequestSerializer
from django.db import IntegrityError

@api_view(['GET'])
def me(request):
    try:
        token = request.headers.get('Authorization').split(' ')[-1]
        decoded_token = AccessToken(token)
        user_id = decoded_token.get('user_id',' ')

        if user_id:
            user = User.objects.get(id=user_id)
            if user:
                return JsonResponse({
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                })
            
            else:
                return Response({'error': 'User not found'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error','Invalid token'},status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(e)
        return Response({'error': 'Token decoding error'},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2')
    })

    if form.is_valid():
        form.save()

        # Send verification email later
    else:
        message = 'error'
    return JsonResponse({'status':message})


@api_view(['POST'])
def send_friend_request(request,pk):
    user = User.objects.get(id=pk)

    try:

        friend_request = FriendshipRequest.objects.create(created_for=user,created_by=request.user)
        friend_request.save()
    except IntegrityError:
        return JsonResponse({'message': 'Friend request already sent'})
    return JsonResponse({'message': 'friend request sent'})

    
@api_view(['GET'])
def friends(request,pk):
    user = User.objects.get(id=pk)
    friends = user.friends.all()

    user_serializer = UserSerializer(user)
    friend_serializer = UserSerializer(friends,many=True)

    if user == request.user:
        friend_request = FriendshipRequest.objects.filter(created_for=user.id,status='Sent')
        friendrequest_serializer = FriendRequestSerializer(friend_request,many=True)
        return JsonResponse({
            'user': user_serializer.data,
            'friends': friend_serializer.data,
            'friend_request': friendrequest_serializer.data,
        })
    else:
        return JsonResponse({
            'user': user_serializer.data,
            'friends': friend_serializer.data,
        })
    
@api_view(['POST'])
def handle_request(request,pk,status):
    user = User.objects.get(pk=pk)
    friend_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friend_request.status = status

    if status == 'accepted':
        request.user.friends.add(user)
        user.friends.add(request.user)
        user.save()
        request.user.save()
        
    friend_request.save()

    return JsonResponse({'message': 'friend request updated'})
