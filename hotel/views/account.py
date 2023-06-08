from django.shortcuts import render, redirect
from django.http import JsonResponse

from hotel.forms.forms import AccountModelForm, AccountAddModelForm
from hotel.models import Account
from hotel.utils.pagination import Pagination


def account_list(request):
	data_dict = {}
	search_data = request.GET.get("q", "")
	search_method = request.GET.get("m", "su")
	if search_data:
		method = {
			"su": "account_user__contains",
			"sp": "account_phone__contains",
			"se": "account_email__contains",
			"si": "id",
		}
		data_dict[method[search_method]] = search_data
	account_data = Account.objects.filter(**data_dict)
	page_object = Pagination(request, account_data, page_size=10)
	page_object.html()
	context = {
		"account_data": page_object.page_queryset,
		"page_string": page_object.page_string,
		"search_data": search_data,
		"search_method": search_method,
		"account_total": Account.objects.all().count(),
	}
	return render(request, "account_list.html", context)


def account_add(request):
	context = {
		"form": None,
		"title": "添加账户信息",
		"addMoreCtr": 1,
		"prv_info": "",
	}
	if request.method == "GET":
		context["form"] = AccountAddModelForm()
		return render(request, "info_edit.html", context)
	# print(request.POST)
	context["form"] = AccountAddModelForm(request.POST)
	if context["form"].is_valid():
		context["form"].save()

		if request.POST.get("addMore") == "1":
			context["form"] = AccountAddModelForm()
			context["prv_info"] = "用户 "+request.POST.get("account_user")+" 已添加"
			return render(request, "info_edit.html", context)
		return redirect("/account/")
	return render(request, "info_edit.html", context)


def account_edit(request, pk):
	context = {
		"form": None,
		"title": "修改账户信息",
		"addmoreCtr": 0,
	}
	if request.method == "GET":
		account_obj = Account.objects.filter(pk=pk).first()
		context["form"] = AccountModelForm(instance=account_obj)
		return render(request, "info_edit.html", context)
	account_obj = Account.objects.filter(pk=pk).first()
	form = AccountModelForm(request.POST, instance=account_obj)
	if form.is_valid():
		form.save()
		return redirect("/account/")
	return render(request, "info_edit.html", context)


def account_del(request):
	uid = request.GET.get("uid")
	if Account.objects.filter(id=uid).exists():
		Account.objects.filter(id=uid).delete()
		return JsonResponse({"status": True, "msg": "删除成功"})
	else:
		return JsonResponse({"status": False, "msg": "删除失败，数据不存在"})


def account_pwd_edit(request):
	return None