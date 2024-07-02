from django.db import models
from categories.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length=50)
    content = models.TextField()
    category = models.ManyToManyField(Category) #ekta post multiple category te thakte pare abar ekta categoryte multiple post thakte pare
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank= True, null=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='comments')
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments By {self.name}"