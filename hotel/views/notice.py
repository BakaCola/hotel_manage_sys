from django.shortcuts import render, redirect
from django.utils import timezone


from hotel.models import Notice
from hotel.forms.forms import NoticeModelForm


def notice_list(request):
	list = Notice.objects.filter(notice_expiration__gte=timezone.now()).order_by("-notice_time")
	return render(request, "notice_list.html", {"list": list})


def notice_detail(request, pk):
	notice = Notice.objects.filter(pk=pk).first()
	return render(request, "notice_detail.html", {"notice": notice})


def notice_manage(request):
	data_dict = {}
	search_data = request.GET.get("q", "")
	search_method = request.GET.get("m", "st")
	if search_data:
		method = {
			"st": "notice_title__contains",
			"sc": "notice_content__contains",
			"sp": "notice_publisher",
		}
		data_dict[method[search_method]] = search_data
	notice = Notice.objects.filter(**data_dict)
	context = {
		"notice": notice,
		"search_data": search_data,
	}
	return render(request, "notice_manage.html", context)


def notice_edit(request, pk):
	if request.method == "GET":
		notice_obj = Notice.objects.filter(pk=pk).first()
		form = NoticeModelForm(instance=notice_obj)
		return render(request, "info_edit.html", {"form": form})
	notice_obj = Notice.objects.filter(pk=pk).first()
	form = NoticeModelForm(request.POST, instance=notice_obj)
	if form.is_valid():
		form.save()
		return redirect("/notice/manage/")
	return render(request, "info_edit.html", {"form": form})


def notice_add(request):
	return None


def notice_del(request):
	return None