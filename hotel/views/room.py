from django.core import serializers
from django.shortcuts import render, redirect
from django.views import View

from hotel.models import Room, RoomType



class RoomList(View):
	def get(self, request):
		room_data = Room.objects.all()
		room_type_data = RoomType.objects.all()
		context = {
			"room_data": room_data,
			"room_type_data": room_type_data,
		}
		return render(request, "room_list.html", context)


class RoomEdit(View):
	def get(request):
		return render(request, "info_edit.html")


class RoomAdd(View):
	def get(request):
		return render(request, "info_edit.html")


class RoomDel(View):
	def get(request):
		return redirect("room_list")