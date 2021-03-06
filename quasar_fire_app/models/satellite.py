from django.core.validators import MinValueValidator
from django.db import models


class Satellite(models.Model):
    name = models.CharField(max_length=30)
    x_position = models.FloatField()
    y_position = models.FloatField()
    distance_from_transmitter = models.FloatField(
        null=True,
        validators=[MinValueValidator(0.0)],
    )
