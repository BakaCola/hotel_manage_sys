"""
URL configuration for mySite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
# from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from hotel.views import auth, index, account, customer, notice, room

urlpatterns = [
	# path("admin/", admin.site.urls),

	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
	path("", index.index),

	path("room/", room.RoomList.as_view()),

	path("room/manage/", room.RoomManageList.as_view()),

	path("notice/", notice.notice_list),
	path("notice/<int:pk>/", notice.notice_detail),

	path("notice/manage/", notice.notice_manage_list),
	path("notice/manage/<int:pk>/edit/", notice.notice_edit),

	path("login/", auth.login),
	path("register/", auth.register),
	path("logout/", auth.logout),

	path("account/", account.account_list),
	path("account/add/", account.account_add),
	path("account/<int:pk>/edit/", account.account_edit),
	path("account/del/", account.account_del),

	path("customer/", customer.customer_list),
	path("customer/add/", customer.customer_add),
	path("customer/<int:pk>/edit/", customer.customer_edit),
	path("customer/<int:pk>/del/", customer.customer_del),
]
