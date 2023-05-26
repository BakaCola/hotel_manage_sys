from django.shortcuts import render, redirect

from hotel.forms.forms import CustomerModelForm
from hotel.models import Customer


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
	customer_data = Customer.objects.filter(**data_dict)
	context = {
		"customer_data": customer_data,
		"search_data": search_data,
		"search_method": search_method,
		"customer_total": Customer.objects.all().count(),
	}
	return render(request, "customer_list.html", context)


def customer_add(request):
	context = {
		"form": None,
		"title": "添加住客信息",
		"addmoreCtr": 1,
		"prv_info": ""
	}
	if request.method == "GET":
		context["form"] = CustomerModelForm()
		return render(request, "info_edit.html", context)
	context["form"] = CustomerModelForm(request.POST)
	if context["form"].is_valid():
		context["form"].save()
		if request.POST.get("addMore") == "1":
			context["form"] = CustomerModelForm()
			context["prv_info"] = "住客 "+request.POST.get("customer_name")+" 已添加"
			return render(request, "info_edit.html", context)
		return redirect("/customer/")
	return render(request, "info_edit.html", context)


def customer_edit(request, pk):
	if request.method == "GET":
		customer_obj = Customer.objects.filter(pk=pk).first()
		form = CustomerModelForm(instance=customer_obj)
		return render(request, "info_edit.html", {"form": form})
	customer_obj = Customer.objects.filter(pk=pk).first()
	form = CustomerModelForm(request.POST, instance=customer_obj)
	if form.is_valid():
		form.save()
		return redirect("/customer/")
	return render(request, "info_edit.html", {"form": form})


def customer_del(request, pk):
	Customer.objects.filter(id=pk).delete()
	return redirect("/customer/")
