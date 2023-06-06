import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

	def process_request(self, request):

		# 遍历白名单中的每个元素
		for pattern in settings.WHITE_LIST:
			# 如果元素是正则表达式，就用re.match来匹配
			if isinstance(pattern, re.Pattern):
				if re.match(pattern, request.path_info):
					return None

		# 否则，检查用户是否已经登录
		info_dict = request.session.get("user")
		if info_dict:
			return None

		# 如果没有登录，就获取用户之前访问的网址
		prev_url = request.path
		# 如果有网址，就把它作为next参数传递给alert视图，并设置code为401
		if prev_url:
			return redirect("/alert/?next=" + prev_url + "&code=401")
		# 如果没有网址，就直接重定向到alert视图，并设置code为404
		else:
			return redirect("/alert/?code=404")