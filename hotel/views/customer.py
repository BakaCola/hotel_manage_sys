from django.shortcuts import render, redirect

from hotel.forms.forms import CustomerModelForm
from hotel.models import Customer
from hotel.utils.pagination import Pagination


def customer_list(request):
	data_dict = {}
	search_data = request.GET.get("q", "")
	search_method = request.GET.get("m", "sn")
	if search_data:
		method = {
			"sn": "customer_name__contains",
			"si": "customer_idNumber__contains",
			"sc": "customer_creator",
			"sp": "customer_phone__contains",
			"se": "customer_email__contains",
		}
		data_dict[method[search_method]] = search_data
	if request.session.get("user")["type"] == 1:
		total = Customer.objects.all().count()
	else:
		data_dict["customer_creator"] = request.session.get("user")["id"]
		total = Customer.objects.filter(**data_dict).count()
	customer_data = Customer.objects.filter(**data_dict)
	page_object = Pagination(request, customer_data, page_size=10)
	page_object.html()
	context = {
		"customer_data": page_object.page_queryset,
		"page_string": page_object.page_string,
		"search_data": search_data,
		"search_method": search_method,
		"customer_total": total,
	}
	return render(request, "customer_list.html", context)


def customer_add(request):
	context = {
		"form": None,
		"title": "添加住客信息",
		"addMoreCtr": 1,
		"prv_info": ""
	}
	if request.method == "GET":
		context["form"] = CustomerModelForm(initial={"customer_creator": request.session.get("user")["id"]})
		return render(request, "info_edit.html", context)
	context["form"] = CustomerModelForm(request.POST)
	if context["form"].is_valid():
		context["form"].save()
		if request.POST.get("addMore") == "1":
			context["form"] = CustomerModelForm()
			context["prv_info"] = "住客 " + request.POST.get("customer_name") + " 已添加"
			return render(request, "info_edit.html", context)
		return redirect("/customer/")
	return render(request, "info_edit.html", context)


def customer_edit(request, pk):
	if request.method == "GET":
		customer_obj = Customer.objects.filter(pk=pk).first()
		form = CustomerModelForm(instance=customer_obj)
		return render(request, "info_edit.html", {"form": form, "title": "修改住客信息"})
	customer_obj = Customer.objects.filter(pk=pk).first()
	form = CustomerModelForm(request.POST, instance=customer_obj)
	if form.is_valid():
		form.save()
		return redirect("/customer/")
	return render(request, "info_edit.html", {"form": form, "title": "修改住客信息"})


def customer_del(request, pk):
	Customer.objects.filter(id=pk).delete()
	return redirect("/customer/")
