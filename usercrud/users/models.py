from django.db import models

# Create your models here.
class AjaxLog(models.Model):
    request_url = models.CharField(max_length=200)
    request_data = models.TextField()
    request_method = models.CharField(max_length=10)
    response_status = models.IntegerField(null=True, blank=True)
    response_data = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

