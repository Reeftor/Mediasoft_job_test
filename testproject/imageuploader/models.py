from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images')
    view_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def update_views(self, image_id):
        self.view_count += 1
        i = Image.objects.get(id=image_id)
        i.view_count = self.view_count
        i.save()
