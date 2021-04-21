from django.db import models


class ConfRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector_availability = models.BooleanField(default=False)

class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(ConfRoom, on_delete=models.CASCADE)
    comment = models.TextField()
