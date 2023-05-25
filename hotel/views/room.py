from django.core import serializers
from django.shortcuts import render, redirect
from django.views import View

from hotel.models import Room


class RoomList(View):
	def get(self, request):
		return render(request, "room_list.html")


class RoomManageList(View):
	def get(self, request):
		return render(request, "room_manage.html")
