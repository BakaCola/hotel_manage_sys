import bcrypt
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from hotel.forms.forms import LoginForm, AccountRegisterModelForm
from hotel.models import Account


class Login(View):
	def get(self, request):
		form = LoginForm()
		return render(request, "login.html", {"form": form})

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			user = Account.objects.filter(account_user=form.cleaned_data["account_user"]).first()
			if user:
				if bcrypt.checkpw(form.cleaned_data["account_password"].encode("utf-8"),
				                  user.account_password.encode("utf-8")):
					request.session["user"] = {'id': user.id, 'type': user.account_type, 'name': user.account_name}
					return redirect("index")
			form.add_error("account_password", "用户名或密码错误")


		return render(request, "login.html", {"form": form})


def register(request):
	form = AccountRegisterModelForm()
	if request.method == "GET":
		return render(request, "register.html", {"form": form})
	form = AccountRegisterModelForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect("login")
	return render(request, "register.html", {"form": form})


def logout(request):
	request.session.flush()
	return redirect("index")


def alert(request):
	code_explain = {
		"401": "您当前未登录！请先登录后在进行操作！",
		"403": "当前用户权限不足！请确认所登录的账户是否有权限访问该页面！",
		"405": "数据恢复失败！",
		"201": "数据恢复成功！"

	}
	code_link = {
		"401": reverse_lazy("login"),
		"405": reverse_lazy("recover_db"),
		"201": reverse_lazy("index"),
	}
	link_text = {
		"401": "登录页",
		"201": "首页",
		"405": "数据恢复页",
	}
	code = request.GET.get("code")
	next_url = request.GET.get("next")
	context = {
		"msg": "您访问的页面不存在！",
		"link": reverse_lazy("index"),
		"link_text": "首页",
	}

	if code in code_explain.keys():
		msg = get_object_or_404(code_explain, code)
		if code in code_link.keys():
			link = get_object_or_404(code_link, code)
			text = get_object_or_404(link_text, code)
		else:
			link = reverse_lazy("index")
			text = "首页"
		context["code_type"] = int(int(code) / 100)
		context["msg"] = msg
		if next_url:
			context["link"] = link + "?next=" + next_url
		else:
			context["link"] = link
		context["link_text"] = text
	if code == "404":
		return HttpResponseNotFound(render(request, "alert.html", context))
	return render(request, "alert.html", context)
