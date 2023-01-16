from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Created Date', default=timezone.now)
    title = models.CharField(verbose_name='Title', max_length=200)
    content = models.TextField(verbose_name='Content')
    slug = models.SlugField(verbose_name='Sluclearg')

    def __str__(self):
        return '"%s" by %s' % (self.title, self.author)
