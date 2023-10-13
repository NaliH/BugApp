import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Bug

# Create your tests here.


class BugModelTests(TestCase):
    def test_was_reported_recently_with_future_bug(self):
        """
        was_reported_recently() returns False for a bug whose
        reported date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_bug = Bug(report_date=time)
        self.assertIs(future_bug.was_reported_recently(), False)

    def test_was_reported_recently_with_old_bug(self):
        """
        was_reported_recently() returns False for a bug whose
        reported date is older than 1 day
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_bug = Bug(report_date=time)
        self.assertIs(old_bug.was_reported_recently(), False)

    def test_was_reported_recently_with_recent_bug(self):
        """
        was_reported_recently() returns True for a bug whose
        reported date is within the past day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_bug = Bug(report_date=time)
        self.assertIs(recent_bug.was_reported_recently(), True)

    def test_bug_time_auto_add_now(self):
        """
        returns True for a bug that has a report time auto added
        """
        bug_report_time_auto = Bug()
        bug_report_time_auto.save()
        self.assertIs(isinstance(bug_report_time_auto.report_date, datetime.datetime), True)


def create_bug(days):
    time = timezone.now() + datetime.timedelta(days=days)
    bug = Bug.objects.create()

    # force the bug to use the specified time
    Bug.objects.filter(pk=bug.pk).update(report_date=time)
    return bug


class BugIndexViewTests(TestCase):

    def test_no_bugs(self):
        """
        If no bugs exists, display an appropriate message
        """
        response = self.client.get(reverse("bug:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No bugs are available.")
        self.assertQuerySetEqual(response.context["latest_bug_list"], [])

    def test_past_bug(self):
        """
        Bugs with a report_date in the past are displayed on the index page
        """
        bug = create_bug(days=-30)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(response.context["latest_bug_list"], [bug],)

    def test_future_bug(self):
        """
        Bugs with a report_date in the future aren't displayed on the index page
        """
        create_bug(days=30)
        response = self.client.get(reverse("bug:index"))
        self.assertContains(response, "No bugs are available.")
        self.assertQuerySetEqual(response.context["latest_bug_list"], [])

    def test_future_bug_and_past_bug(self):
        """
        If both a bug with a future report_date and a past report_date exists,
        only the past bug is displayed
        """
        bug = create_bug(days=-30)
        create_bug(days=30)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(response.context["latest_bug_list"], [bug], )

    def test_multiple_past_bugs(self):
        """
        Multiple bugs can be displayed
        """
        bug1 = create_bug(days=-30)
        bug2 = create_bug(days=-15)
        bug3 = create_bug(days=-5)
        bug4 = create_bug(days=-1)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(response.context["latest_bug_list"], [bug1, bug2, bug3, bug4], )


