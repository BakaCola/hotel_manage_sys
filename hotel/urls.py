from django.urls import path
from .views import index, auth, account, customer, notice, room

urlpatterns = [
	path("", index.index, name="index"),

	path("book/", room.RoomList.as_view(), name="book_list"),

	path("room/", room.RoomManageList.as_view(), name="room_list"),

	path("notice/", notice.notice_list, name="notice_list"),
	path("notice/<int:pk>/", notice.notice_detail, name="notice_detail"),

	path("notice/manage/", notice.notice_manage, name="notice_manage"),
	path("notice/manage/add/", notice.notice_add, name="notice_add"),
	path("notice/manage/<int:pk>/edit/", notice.notice_edit, name="notice_edit"),
	path("notice/manage/<int:pk>/del/", notice.notice_del, name="notice_del"),

	path("login/", auth.login, name="login"),
	path("register/", auth.register, name="register"),
	path("logout/", auth.logout, name="logout"),

	path("account/", account.account_list, name="account_list"),
	path("account/add/", account.account_add, name="account_add"),
	path("account/<int:pk>/edit/", account.account_edit, name="account_edit"),
	path("account/<int:pk>/pwdedit/", account.account_pwd_edit, name="account_pwd_edit"),
	path("account/del/", account.account_del, name="account_del"),

	path("customer/", customer.customer_list, name="customer_list"),
	path("customer/add/", customer.customer_add, name="customer_add"),
	path("customer/<int:pk>/edit/", customer.customer_edit, name="customer_edit"),
	path("customer/<int:pk>/del/", customer.customer_del, name="customer_del"),

]
