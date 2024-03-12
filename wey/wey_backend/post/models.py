from django.db import models
import uuid
from account.models import User
from django.utils.timesince import timesince

class Like(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_by = models.ForeignKey(User,related_name='likes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    images = models.ImageField(upload_to='post_attachments',blank=True,null=True)
    created_by = models.ForeignKey(User,related_name='post_attachments',on_delete=models.CASCADE)

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    body = models.TextField(blank=True,null=True)
    attachments = models.ManyToManyField(PostAttachment,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='post',on_delete=models.CASCADE)

    likes = models.ManyToManyField(Like,blank=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.created_by.name}"
    
    def created_at_formatted(self):
        return timesince(self.created_at)

    



