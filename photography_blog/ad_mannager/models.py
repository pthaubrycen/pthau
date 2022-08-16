from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=25)

    def __str__(self):
        return self.category_name

class Status(models.Model):
    status_name = models.CharField(max_length=25)
    
    def __str__(self):
        return self.status_name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    thumbnail = models.FileField(upload_to="thumbnail image")
    slug = models.SlugField(null=False, unique=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    isDelete = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True)
    task = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    birthday = models.DateField(null=True)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username