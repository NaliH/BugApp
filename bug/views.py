from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.template import loader
from .models import Bug

# Create your views here.


def index(request):
    latest_bugs_list = Bug.objects.order_by("report_date")[:5]
    context = {"latest_bug_list": latest_bugs_list}
    return render(request, "bug/index.html", context)


def report(request):
    new_bug = Bug()
    try:
        bug_description = request.POST["desc"]
    except KeyError:
        return render(request, "bug/report.html", {
            "new_bug": new_bug,
            "error_message": "You didn't enter a description"
        },)
    else:
        new_bug.description_text = bug_description
        new_bug.save()

    try:
        bug_type = request.POST["type"]
    except KeyError:
        return render(request, "bug/report.html", {
            "new_bug": new_bug,
            "error_message": "You didn't enter a bug type"
        },)
    else:
        new_bug.bug_type_text = bug_type
        new_bug.save()

    try:
        bug_status = request.POST["status"]
    except KeyError:
        return render(request, "bug/report.html", {
            "new_bug": new_bug,
            "error_message": "You didn't select a bug status"
        },)
    else:
        new_bug.status_text = bug_status
        new_bug.save()

    return HttpResponseRedirect(reverse("bug:detail", args=(new_bug.id,)))


def detail(request, bug_id):
    bug = get_object_or_404(Bug, pk=bug_id)
    return render(request, "bug/detail.html", {"bug": bug})


def list_bugs(request):
    #bug_list = get_list_or_404(Bug, id__isnull=False)
    bug_list = Bug.objects.all()
    context = {"bug_list": bug_list}
    return render(request, "bug/list.html", context)
