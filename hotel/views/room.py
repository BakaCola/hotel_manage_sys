from django.core import serializers
from django.shortcuts import render, redirect
from django.views import View

from hotel.forms.forms import RoomModelForm, RoomTypeModelForm
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
	context = {
		"title": "修改账户信息",
		"addmoreCtr": 0,
		"prv_info": "",
	}

	def get(self, request, pk):
		room_obj = Room.objects.filter(pk=pk).first()
		self.context["form"] = RoomModelForm(instance=room_obj)
		return render(request, "info_edit.html", self.context)


class RoomAdd(View):
	context = {
		"title": "添加客房信息",
		"addMoreCtr": 1,
		"prv_info": "",
	}

	def get(self, request):
		self.context["form"] = RoomModelForm()
		return render(request, "info_edit.html", self.context)

	def post(self, request):
		# print(request.POST)
		form = RoomModelForm(request.POST)
		if form.is_valid():
			form.save()
			if request.POST.get("addMore") == "1":
				self.context["form"] = RoomModelForm()
				self.context["prv_info"] = "客房 " + request.POST.get("room_number") + " 已添加"
				return render(request, "info_edit.html", self.context)
			return redirect("room_list")
		self.context["form"] = form
		return render(request, "info_edit.html", self.context)


class RoomDel(View):
	def get(self, request):
		return redirect("room_list")


class RoomTypeAdd(View):
	context = {
		"title": "添加房型信息",
		"addMoreCtr": 1,
		"prv_info": "",
	}

	def get(self, request):
		self.context["form"] = RoomTypeModelForm()
		return render(request, "info_edit.html", self.context)

	def post(self, request):
		# print(request.POST)
		form = RoomTypeModelForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			if request.POST.get("addMore") == "1":
				self.context["form"] = RoomTypeModelForm()
				self.context["prv_info"] = "房型 " + request.POST.get("roomType_name") + " 已添加"
				return render(request, "info_edit.html", self.context)
			return redirect("room_list")
		self.context["form"] = form
		return render(request, "info_edit.html", self.context)
