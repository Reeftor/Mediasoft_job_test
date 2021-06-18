from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
