from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from articles.models import Article
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(1000)
        ]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE,default=None, null=True, blank=True)

    def __str__(self):
        return self.content