from django.shortcuts import render, redirect
from django.views import View

from hotel.models import Order


class OrderList(View):
	def get(self, request):
		data_dict = {}
		if request.session.get("user")['type'] == 1:
			order = Order.objects.all()
			order_total = Order.objects.all().count()
		else:
			data_dict["order_creator"] = request.session.get("user")["id"]
			order = Order.objects.filter(**data_dict)
			order_total = Order.objects.filter(**data_dict).count()
		context = {
			"order_data": order,
			"order_total": order_total
		}
		return render(request, "order_list.html", context)
