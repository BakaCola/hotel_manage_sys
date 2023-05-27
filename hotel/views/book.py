from django.shortcuts import render, redirect
from django.views import View

from hotel.models import Room


class BookList(View):
	def get(self, request):
		room_data = Room.objects.all()
		return render(request, "book_list.html", {"room_data": room_data})


