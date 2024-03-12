from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = extra_fields.get('is_staff',False)
        user.is_superuser = extra_fields.get('is_superuser',False)
        user.save(using=self._db)
        return user
    
    def super_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)
    

class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30,blank=True)
    avatar = models.ImageField(upload_to='avatars',blank=True,null=True)
    friends = models.ManyToManyField('self')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    @property
    def friends_count(self):
        return self.friends.count()

    def __str__(self):
        return self.email
    
# class Friendship(models.Model):
#     from_user = models.ForeignKey('User',on_delete=models.CASCADE,related_name = 'friendship_from_user')
#     to_user = models.ForeignKey('User',on_delete=models.CASCADE,related_name = 'friendship_to_user')

#     class Meta:
#         constraints = [models.UniqueConstraint(fields=['from_user','to_user'],name='unique_friendship')]



class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User,related_name='received_friendshiprequests',on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='created_friendshiprequest',on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default =SENT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['created_by','created_for'],name='unique_constraint')]