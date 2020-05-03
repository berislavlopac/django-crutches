# -*- coding: utf-8 -*-

### gravatar.py ###############
### place inside a 'templatetags' directory inside the top level of a Django app (not project, must be inside an app)
### at the top of your page template include this:
### {% load gravatar %}
### and to use the url do this:
### <img src="{% gravatar_url 'someone@somewhere.com' %}">
### or
### <img src="{% gravatar_url sometemplatevariable %}">
### just make sure to update the "default" image path below

import hashlib
import urllib

from django import template
from django.conf import settings

register = template.Library()


class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ""
        size = getattr(settings, "GRAVATAR_SIZE", 60)
        default = getattr(
            settings,
            "GRAVATAR_DEFAULT_URL",
            "http://ultramotor.evra.codegent.com/images/icons/default_avatar.gif",
        )
        gravatar_url = (
            "http://www.gravatar.com/avatar/"
            + hashlib.md5(email.lower()).hexdigest()
            + "?"
        )
        gravatar_url += urllib.urlencode({"d": default, "s": str(size)})
        return gravatar_url


@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires a single argument"
        )
    return GravatarUrlNode(email)
