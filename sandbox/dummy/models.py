from django.db import models


class Dummy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
