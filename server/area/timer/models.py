from django.db import models
from django.utils import timezone
from services.models import Service

# Create a model used to detect if the date time is passed (with minutes, hours, days, months, years)
class Timer(models.Model):
    date_time = models.DateTimeField()
    is_passed = models.BooleanField(default=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.date_time)

    def save(self, *args, **kwargs):
        if self.date_time < timezone.now():
            self.is_passed = True
        else:
            self.is_passed = False
        super(Timer, self).save(*args, **kwargs)