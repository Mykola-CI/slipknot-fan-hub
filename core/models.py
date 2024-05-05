from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    description = models.TextField()
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title
