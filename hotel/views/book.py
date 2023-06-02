from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from hotel.models import Room, RoomType


class BookList(View):
	context = {
		"room_type": RoomType.objects.all(),
		"today": timezone.now().date(),
	}

	def get(self, request):
		return render(request, "book_list.html", self.context)
		pass


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
