from django.db import models
from django.contrib.auth.models import User

class RecordMaster(models.Model):
    website_name = models.CharField(max_length=255)
    website_url=models.CharField(max_length=255,blank=True,null=True)
    website_username = models.CharField(max_length=50)
    website_password = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return self.website_name