import datetime

from django.db import models
from django.utils import timezone


class Bug(models.Model):
    description_text = models.CharField(max_length=200)
    bug_type_text = models.CharField(max_length=200)
    report_date = models.DateTimeField(auto_now_add=True)
    status_text = models.CharField(max_length=50)

    def was_reported_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.report_date <= now

    def __str__(self):
        return self.bug_type_text
