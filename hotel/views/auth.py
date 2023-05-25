from django.shortcuts import render


def login(request):
	if request.method == "GET":
		return render(request, "login.html")
	print(request.POST)

	user = request.POST.get("user")
	pwd = request.POST.get("pwd")
	if user == "" or pwd == "":
		return render(request, "login.html", {"err_msg": "用户名或密码不能为空"})
	if user == "admin@qq.com" and pwd == "123456":

		return render(request, "account_list.html")
	return render(request, "index.html")


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
	return None