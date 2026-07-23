from django.db import models
import uuid
# Create your models here.
class videos(models.Model):
    video_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_path = models.CharField(max_length=200)



class transcribes(models.Model):
    v_id=models.ForeignKey(videos,on_delete=models.CASCADE,to_field="video_id")
    start=models.DurationField(null=True)
    end=models.DurationField(null=True)
    text = models.TextField()
