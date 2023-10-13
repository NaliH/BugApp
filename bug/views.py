from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from django.template import loader
from .models import Bug

# Create your views here.


class IndexView(generic.ListView):
    template_name = "bug/index.html"
    context_object_name = "latest_bug_list"

    def get_queryset(self):
        """
        Return the 5 latest bug reports.
        """
        return Bug.objects.filter(report_date__lte=timezone.now()).order_by("report_date")[:5]


def report(request):
    new_bug = Bug()
    if request.method == "POST":
        try:
            bug_description = request.POST['desc']
            if not bug_description:
                raise ValueError
        except (KeyError, ValueError):
            return render(request, "bug/report.html", {
                "new_bug": new_bug,
                "check_status": request.POST['status'],
                "fill_type": request.POST['type'],
                "error_message": "You didn't enter a description"
            },)
        else:
            new_bug.description_text = bug_description

        try:
            bug_type = request.POST['type']
            if not bug_type:
                raise ValueError
        except (KeyError, ValueError):
            return render(request, "bug/report.html", {
                "new_bug": new_bug,
                "fill_desc": request.POST['desc'],
                "check_status": request.POST['status'],
                "error_message": "You didn't enter a bug type"
            },)
        else:
            new_bug.bug_type_text = bug_type

        try:
            bug_status = request.POST['status']
            if not bug_status:
                raise ValueError
        except (KeyError, ValueError):
            return render(request, "bug/report.html", {
                "new_bug": new_bug,
                "fill_desc": request.POST['desc'],
                "fill_type": request.POST['type'],
                "error_message": "You didn't select a bug status"
            },)
        else:
            new_bug.status_text = bug_status
            new_bug.save()
            return HttpResponseRedirect(reverse("bug:detail", args=(new_bug.id,)))
    else:

        return render(request, "bug/report.html", {"new_bug": new_bug})


class DetailView(generic.DetailView):
    model = Bug
    template_name = "bug/detail.html"


class ListView(generic.ListView):
    template_name = "bug/list.html"
    context_object_name = "bug_list"

    def get_queryset(self):
        return Bug.objects.all()
