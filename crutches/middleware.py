from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import resolve
from django.utils.translation import activate

import re

REQUIRED_URLS = []
if hasattr(settings, "LOGIN_REQUIRED_URLS"):
    REQUIRED_URLS = settings.LOGIN_REQUIRED_URLS


class RequireLoginMiddleware(object):
    """Requires login for URLs defined in REQUIRED_URLS setting."""

    def __init__(self):
        self.urls = tuple([re.compile(url) for url in REQUIRED_URLS])
        self.require_login_path = getattr(settings, "LOGIN_URL", "/accounts/login/")

    def process_request(self, request):
        if request.user.is_anonymous() and request.path != self.require_login_path:
            for url in self.urls:
                if url.match(request.path):
                    return HttpResponseRedirect(
                        u"{0}?next={1}".format(self.require_login_path, request.path)
                    )


class DisableI18nMiddleware:
    def process_request(self, request):
        apps = ["admin", "filebrowser", "rosetta", "rosetta-grappelli"]
        urls = ["rosetta"]
        resolver_match = resolve(request.path)
        if resolver_match.app_name in apps or any(
            resolver_match.url_name.startswith(url) for url in urls
        ):
            activate(settings.LANGUAGES[0][0])
