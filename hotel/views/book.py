from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from hotel.models import Room, RoomType, OrderDetail


def get_available(start, end, room_type_id):
	all_room = Room.objects.filter(room_type_id=room_type_id)
	booked_room = OrderDetail.objects.filter(order__order_check_in__lte=end,
	                                         order__order_check_out__gte=start).values_list('room', flat=True)
	available_room = all_room.exclude(id__in=booked_room)
	# available_room_numbers = available_room.values_list('room_number', flat=True)
	return available_room


class BookList(View):

	def get(self, request):
		roomType_data = RoomType.objects.all()
		room_count = []
		today = timezone.now().strftime("%Y-%m-%d")
		tomorrow = (timezone.now() + timezone.timedelta(days=1)).strftime("%Y-%m-%d")
		st = request.GET.get("st", today)
		ed = request.GET.get("ed", today)
		for room_type in roomType_data:
			room_count.append(get_available(st, ed, room_type.id).count())
		context = {
			"roomType_data": zip(roomType_data, room_count),
			"st": st,
			"ed": ed,
			"today": today,
			"tomorrow": tomorrow
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
		room_type = RoomType.objects.all()
		return render(request, "book_check.html", {"room_type": room_type})
		pass


class BookDetail(View):
	def get(self, request):
		room_type = RoomType.objects.all()
		return render(request, "book_detail.html", {"room_type": room_type})
		pass
