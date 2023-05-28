from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):

	def process_request(self, request):

		blank_list = ["/login/", "/register/", "/logout/", "/", "/notice/", "/notice_detail/", "/book/", "/alert/"]

		if request.path_info in blank_list:
			return

		info_dict = request.session.get("user")
		if info_dict:
			return

		return redirect("/alert/?code=401")
