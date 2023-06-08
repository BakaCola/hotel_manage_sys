from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic import DetailView

from hotel.models import Order, OrderDetail, Room


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


class OrderDetailView(DetailView):  # 继承DetailView类
	model = Order  # 指定模型为Order
	template_name = 'order_detail.html'  # 指定模板文件为order_detail.html
	context_object_name = 'order'  # 指定上下文对象的名称为order

	def get_context_data(self, **kwargs):  # 重写get_context_data方法
		context = super().get_context_data(**kwargs)  # 调用父类的方法，获取默认的上下文数据
		context['order_details'] = self.object.orderdetail_set.all()  # 获取订单对应的所有订单详细对象，并添加到上下文数据中
		return context  # 返回上下文数据


def orderSetStatus(request):
	if request.method == "GET":
		order_id = request.GET.get("id")
		order_status = request.GET.get("status")
		order_obj = Order.objects.filter(pk=order_id).first()
		order_obj.order_status = order_status
		order_obj.save()
		od = OrderDetail.objects.filter(order_id=order_id)
		for i in od:
			room_obj = Room.objects.filter(pk=i.room_id).first()
			if order_status == "1":
				room_obj.room_status = 1
			else:
				room_obj.room_status = 0
			room_obj.save()


		return redirect("/order/")
