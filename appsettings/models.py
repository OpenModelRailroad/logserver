from django.db import models


# Create your models here.
class Appsettings(models.Model):
    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.key
