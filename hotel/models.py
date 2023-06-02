from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class Room(models.Model):
	room_number = models.CharField(verbose_name="客房号", max_length=10, unique=True)
	room_type = models.ForeignKey(verbose_name="客房类型", to="RoomType", on_delete=models.SET_NULL, null=True,
	                              blank=True)
	room_status = models.SmallIntegerField(verbose_name="客房状态", choices=((0, "空闲"), (1, "已预订"), (2, "已入住")),
	                                       default=0)

	def __str__(self):
		return self.room_number


class Customer(models.Model):
	customer_idNumber = models.CharField(verbose_name="身份证号", max_length=18)
	customer_creator = models.ForeignKey(verbose_name="住客创建人", to="Account", on_delete=models.CASCADE)
	customer_name = models.CharField(verbose_name="姓名", max_length=10)
	customer_phone = models.CharField(verbose_name="电话号码", max_length=11)
	customer_email = models.EmailField(verbose_name="邮箱")
	customer_status = models.SmallIntegerField(verbose_name="状态", choices=((0, "正常"), (1, "已封禁")), default=0)


class Order(models.Model):
	order_idNumber = models.CharField(verbose_name="订单号", max_length=18)
	order_creator = models.ForeignKey(verbose_name="订单创建人", to="Account", on_delete=models.CASCADE)
	order_time = models.DateTimeField(verbose_name="下单时间", auto_now_add=True)
	order_check_in = models.DateField(verbose_name="住房起始日期")
	order_check_out = models.DateField(verbose_name="住房结束日期")
	order_status = models.SmallIntegerField(verbose_name="订单状态", default=0,
	                                        choices=((0, "已预订"), (1, "已入住"), (2, "已完成"), (3, "已取消")))
	order_price = models.DecimalField(verbose_name="订单价格", max_digits=8, decimal_places=2)
	order_rooms = models.ManyToManyField(verbose_name="订单房间", to="Room", through="OrderDetail")


class Account(models.Model):
	account_user = models.CharField(verbose_name="账户名", max_length=32, unique=True)
	account_name = models.CharField(verbose_name="昵称", max_length=32)
	account_phone = models.CharField(verbose_name="电话号码", max_length=11, unique=True)
	account_email = models.EmailField(verbose_name="邮箱", unique=True)
	account_password = models.CharField(verbose_name="密码", max_length=255)
	account_type = models.SmallIntegerField(verbose_name="账户类型", choices=((0, "顾客"), (1, "管理员")), default=0)
	account_status = models.SmallIntegerField(verbose_name="账户状态", choices=((0, "正常"), (1, "已封禁")), default=0)

	def __str__(self):
		return self.account_user


class Notice(models.Model):
	notice_title = models.CharField(verbose_name="通知标题", max_length=40)
	notice_content = models.TextField(verbose_name="通知内容", max_length=300)
	notice_time = models.DateTimeField(verbose_name="发布时间", default=timezone.now)
	notice_expiration = models.DateTimeField(verbose_name="失效时间")
	notice_publisher = models.ForeignKey(verbose_name="发布人", to="Account", on_delete=models.CASCADE,
	                                     limit_choices_to={"account_type": 1})


class OrderDetail(models.Model):
	order = models.ForeignKey(verbose_name="订单", to="Order", on_delete=models.CASCADE)
	customer = models.ForeignKey(verbose_name="顾客", to="Customer", on_delete=models.CASCADE)
	room = models.ForeignKey(verbose_name="房间", to="Room", on_delete=models.CASCADE)


class RoomType(models.Model):
	roomType_name = models.CharField(verbose_name="客房类型", max_length=10)
	roomType_price = models.DecimalField(verbose_name="客房价格", max_digits=8, decimal_places=2)
	roomType_description = models.TextField(verbose_name="客房描述")
	roomType_img = models.ImageField(verbose_name="客房图片", upload_to="rooms_img/")

	def __str__(self):
		return self.roomType_name

	def get_absolute_url(self):
		return reverse("hotel:room_detail", kwargs={"pk": self.pk})

