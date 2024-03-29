from django.core import serializers
from django.shortcuts import render, redirect
from django.views import View

from hotel.forms.forms import RoomModelForm, RoomTypeModelForm
from hotel.models import Room, RoomType
from hotel.utils.pagination import Pagination


class RoomList(View):
	def get(self, request):
		room_data = Room.objects.all()
		room_type_data = RoomType.objects.all()
		page_object_room = Pagination(request, room_data, page_size=10)
		page_object_roomType = Pagination(request, room_type_data, page_size=10, page_param="tPage")
		page_object_room.html()
		page_object_roomType.html()
		context = {
			"room_data": page_object_room.page_queryset,
			"room_type_data": page_object_roomType.page_queryset,
			"page_string_room": page_object_room.page_string,
			"page_string_roomType": page_object_roomType.page_string,
			"room_total": room_data.count(),
			"room_type_total": room_type_data.count(),
		}
		return render(request, "room_list.html", context)


class RoomEdit(View):
	context = {
		"title": "修改客房信息",
		"addmoreCtr": 0,
		"prv_info": "",
	}

	def get(self, request, pk):
		room_obj = Room.objects.filter(pk=pk).first()
		self.context["form"] = RoomModelForm(instance=room_obj)
		return render(request, "info_edit.html", self.context)

	def post(self, request, pk):
		room_obj = Room.objects.filter(pk=pk).first()
		form = RoomModelForm(request.POST, instance=room_obj)
		if form.is_valid():
			form.save()
			return redirect("room_list")
		self.context["form"] = form
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
		pk = request.GET.get("pk")
		room_obj = Room.objects.filter(pk=pk).first()
		room_obj.delete()
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


class RoomTypeEdit(View):
	context = {
		"title": "修改房型信息",
		"addmoreCtr": 0,
		"prv_info": "",
	}

	def get(self, request, pk):
		room_type_obj = RoomType.objects.filter(pk=pk).first()
		self.context["form"] = RoomTypeModelForm(instance=room_type_obj)
		return render(request, "info_edit.html", self.context)

	def post(self, request, pk):
		room_type_obj = RoomType.objects.filter(pk=pk).first()
		form = RoomTypeModelForm(request.POST, request.FILES, instance=room_type_obj)
		if form.is_valid():
			form.save()
			return redirect("room_list")
		self.context["form"] = form
		return render(request, "info_edit.html", self.context)


class RoomTypeDel(View):
	def get(self, request):
		pk = request.GET.get("pk")
		room_type_obj = RoomType.objects.filter(pk=pk).first()
		room_type_obj.delete()
		return redirect("room_list")