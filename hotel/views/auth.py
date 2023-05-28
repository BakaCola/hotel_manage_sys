import bcrypt
from django.shortcuts import render, redirect
from django.views import View

from hotel.forms.forms import LoginForm
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
				if bcrypt.checkpw(form.cleaned_data["account_password"].encode("utf-8"), user.account_password.encode("utf-8")):
					request.session["user"] = {'id': user.id, 'type': user.account_type, 'name': user.account_name}
					return redirect("index")
		form.add_error("account_password", "用户名或密码错误")
		return render(request, "login.html", {"form": form})


def register(request):
	if request.method == "GET":
		return render(request, "register.html")
	elif request.method == "POST":
		print(request.POST)
		user = request.POST.get("user")
		pwd = request.POST.get("pwd")
		pwd2 = request.POST.get("pwd2")
		if pwd == pwd2:
			return render(request, "login.html", {"msg": "注册成功"})
		else:
			return render(request, "register.html", {"msg": "两次密码不一致"})


def logout(request):
	request.session.flush()
	return redirect("index")

def alert(request):
	code_explain = {
		"401": "您当前未登录！请先登录后在进行操作！",
		"403": "当前用户权限不足！请确认所登录的账户是否有权限访问该页面！",
		"404": "您所访问的页面不存在！",
	}
	code_link = {
		"401": "/login/",
	}
	link_text = {
		"401": "登录页",
	}
	code = request.GET.get("code")
	if code in code_explain.keys():
		msg = code_explain.get(code)
		if code in code_link.keys():
			link = code_link.get(code)
			text = link_text.get(code)
		else:
			link = "/"
			text = "首页"
		return render(request, "alert.html", {"msg": msg, "link": link, "link_text": text})
	return render(request, "alert.html", {"msg": code_explain["404"], "link": "/", "link_text": "首页"})
