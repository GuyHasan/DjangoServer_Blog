from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator

# Create your models here.

class Comment(models.Model):
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
    content = models.TextField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(300)
        ]
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE,default=None, null=True, blank=True)

    def __str__(self):
        return self.content