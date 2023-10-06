import datetime

from django.db import models
from django.utils import timezone


class Bug(models.Model):
    description_text = models.CharField(max_length=200)
    bug_type_text = models.CharField(max_length=200)
    report_date = models.DateTimeField()
    status_text = models.CharField(max_length=50)

    def was_reported_recently(self):
        return self.report_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.bug_type_text
