# from django.conf import settings
# import re
# from django.shortcuts import redirect

# EXEMPT_URLS = []
# EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXCEPT_URLS]


# class trial:


# 	def process_view(self, request, view_func, view_args, view_kwargs):
# 		assert hasattr(request, 'user')
# 		path = request.path_info.lstrip('/')

# 		if not request.user.is_authenticated:
# 			if not any(url.match(path) for url in EXEMPT_URLS ):
# 				return redirect(settings.LOGIN_URL)