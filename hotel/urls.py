from django.urls import path
from .views import index, auth, account, customer, notice, room, book, order, sql
from .views import test

urlpatterns = [
	path("", index.index, name="index"),

	path("test/", test.test),

	path("book/", book.BookList.as_view(), name="book_list"),
	path("book/detail/", book.book_detail, name="book_detail"),
	path("book/check/", book.BookCheck.as_view(), name="book_check"),

	path("order/", order.OrderList.as_view(), name="order_list"),
	path("order/<int:pk>/detail/", order.OrderDetailView.as_view(), name="order_detail"),
	path("order/setStatus/", order.orderSetStatus, name="order_set_status"),

	path("room/", room.RoomList.as_view(), name="room_list"),
	path("room/add/", room.RoomAdd.as_view(), name="room_add"),
	path("room/<int:pk>/edit/", room.RoomEdit.as_view(), name="room_edit"),
	path("room/del/", room.RoomDel.as_view(), name="room_del"),

	path("roomtype/add/", room.RoomTypeAdd.as_view(), name="room_type_add"),
	path("roomtype/<int:pk>/edit/", room.RoomTypeEdit.as_view(), name="room_type_edit"),
	path("roomtype/del/", room.RoomTypeDel.as_view(), name="room_type_del"),

	path("notice/", notice.notice_list, name="notice_list"),
	path("notice/<int:pk>/", notice.notice_detail, name="notice_detail"),

	path("notice/manage/", notice.notice_manage, name="notice_manage"),
	path("notice/manage/add/", notice.NoticeAdd.as_view(), name="notice_add"),
	path("notice/manage/<int:pk>/edit/", notice.notice_edit, name="notice_edit"),
	path("notice/manage/<int:pk>/del/", notice.notice_del, name="notice_del"),

	path("login/", auth.Login.as_view(), name="login"),
	path("register/", auth.register, name="register"),
	path("logout/", auth.logout, name="logout"),
	path("alert/", auth.alert, name="alert"),

	path("account/", account.account_list, name="account_list"),
	path("account/add/", account.account_add, name="account_add"),
	path("account/<int:pk>/edit/", account.account_edit, name="account_edit"),
	path("account/<int:pk>/pwdedit/", account.account_pwd_edit, name="account_pwd_edit"),
	path("account/del/", account.account_del, name="account_del"),

	path("customer/", customer.customer_list, name="customer_list"),
	path("customer/add/", customer.customer_add, name="customer_add"),
	path("customer/<int:pk>/edit/", customer.customer_edit, name="customer_edit"),
	path("customer/<int:pk>/del/", customer.customer_del, name="customer_del"),

	path("db/", sql.recover_db, name="recover_db"),
	path("db/backup/", sql.backup_db, name="backup_db"),

]
