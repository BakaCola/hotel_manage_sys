from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from hotel.models import Room, RoomType, OrderDetail, Customer, Order


def get_available(start, end, room_type_id):
	all_room = Room.objects.filter(room_type_id=room_type_id)
	booked_room = OrderDetail.objects.filter(order__order_check_in__lt=end,
	                                         order__order_check_out__gt=start).values_list('room', flat=True)
	available_room = all_room.exclude(id__in=booked_room)
	# available_room_numbers = available_room.values_list('room_number', flat=True)
	return available_room


class BookList(View):

	def get(self, request):
		roomType_data = RoomType.objects.all()
		room_count = []
		today = timezone.now().strftime("%Y-%m-%d")
		tomorrow = (timezone.now() + timezone.timedelta(days=1)).strftime("%Y-%m-%d")
		error = request.GET.get("error", "")
		for room_type in roomType_data:
			room_count.append(get_available(today, tomorrow, room_type.id).count())
		context = {
			"roomType_data": zip(roomType_data, room_count),
			"today": today,
			"tomorrow": tomorrow,
			"error": error
		}
		return render(request, "book_list.html", context)

	def post(self, request):
		st = request.POST.get("st")
		ed = request.POST.get("ed")
		roomType_data = RoomType.objects.all()
		room_count = {}
		for room_type in roomType_data:
			room_count[room_type.id] = get_available(st, ed, room_type.id).count()
		# print(room_count)
		return JsonResponse({"room_availability": room_count})


class BookCheck(View):
	def get(self, request):
		book = request.session.get("book")
		room_type = RoomType.objects.filter(id=book["type_id"]).first()
		day = (timezone.datetime.strptime(book["ed"], "%Y-%m-%d") - timezone.datetime.strptime(book["st"],
		                                                                                       "%Y-%m-%d")).days
		context = {
			"room_type": room_type,
			"st": book["st"],
			"ed": book["ed"],
			"num": str(book["num"]),
			"price": int(book["num"]) * room_type.roomType_price * day,
			"customer_list": Customer.objects.filter(customer_creator_id=request.session.get("user")["id"]),
			"day": day
		}

		return render(request, "book_check.html", context)

	@transaction.atomic
	def post(self, request):
		# print(request.POST)
		book = request.session.get("book")
		st = book["st"]
		ed = book["ed"]
		num = int(book["num"])
		day = (timezone.datetime.strptime(ed, "%Y-%m-%d") - timezone.datetime.strptime(st, "%Y-%m-%d")).days
		room_type = RoomType.objects.filter(id=book["type_id"]).first()
		room = get_available(st, ed, room_type.id)
		if len(room) < num:
			return redirect("/book/?st=" + st + "&ed=" + ed + "&num=" + str(num) + "&error=3")
		now = timezone.datetime.now()
		order_id = now.strftime("%Y%m%d%H%M%S%f")
		price = int(book["num"]) * room_type.roomType_price * day
		order = Order.objects.create(order_idNumber=order_id, order_time=now, order_check_in=st,
		                             order_check_out=ed,
		                             order_status=0, order_price=price,
		                             order_creator_id=request.session.get("user")["id"])
		# print(order_id, now, st, ed, 0, price, request.session.get("user")["id"])
		for i in range(1, int(book["num"]) + 1):
			getStr = "room_" + str(i)
			customer_list = request.POST.getlist(getStr)
			for customer_id in customer_list:
				# print(customer_id, order_id, room[i - 1].id)
				OrderDetail.objects.create(customer_id=customer_id, order=order, room=room[i - 1])

		return redirect("/order/")


@csrf_exempt
def book_detail(request):
	# 获取post请求中的数据
	type_id = request.POST.get("type_id")
	st = request.POST.get("st")
	ed = request.POST.get("ed")
	num = int(request.POST.get("num"))
	if num > 5 or num < 1:
		return JsonResponse({"error": "1"})
	if st < timezone.now().strftime("%Y-%m-%d") or ed < st:
		return JsonResponse({"error": "2"})
	if num > get_available(st, ed, type_id).count():
		return JsonResponse({"error": "3"})

	request.session["book"] = {
		"type_id": type_id,
		"st": st,
		"ed": ed,
		"num": num
	}
	# 返回一个json响应，指向订单详细页的url
	return JsonResponse({"url": "/book/check/"})
