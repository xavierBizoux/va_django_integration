import uuid

from django.db import models
from django.utils import timezone


# Create your models here.
class ScoredData(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Type = models.CharField(max_length=30)
    DriveTrain = models.CharField(max_length=30)
    EngineSize = models.FloatField()
    Cylinders = models.IntegerField()
    Horsepower = models.IntegerField()
    MPG_City = models.FloatField()
    Weight = models.FloatField()
    Wheelbase = models.IntegerField()
    P_MSRP = models.FloatField()
    Created_At = models.DateTimeField(default=timezone.now, editable=False)
