from django.shortcuts import render
from django.utils import timezone

from hotel.models import Notice


def index(request):
	last_notice = Notice.objects.filter(notice_expiration__gte=timezone.now()).order_by("-notice_time")

	return render(request, "index.html", {"notice": last_notice})
