# -*- coding: utf-8 -*-

import re
from datetime import date
from django.conf import settings
from django import template
from django.utils.http import urlencode
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.flatpages.models import FlatPage

register = template.Library()

# base_url
def do_base_url(parser, token):
    try:
        tag_name, path = token.split_contents()
    except ValueError:
        path = ""
    if path != "" and not (path[0] == path[-1] and path[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return BaseUrlNode(path[1:-1])


class BaseUrlNode(template.Node):
    def __init__(self, path):
        self.path = path

    def render(self, context):
        request = context["request"]
        return "http://" + request.get_host()


register.tag("base_url", do_base_url)

# settings value
@register.simple_tag
def settings_value(name):
    try:
        return settings.__getattr__(name)
    except AttributeError:
        return ""


# copyright notice
@register.simple_tag
def copyright_notice(starting_year):
    current_year = date.today().year
    if starting_year == current_year:
        years = current_year
    else:
        years = "%d-%d" % (starting_year, current_year)
    return "&copy; %s" % years


# list of links
@register.simple_tag
def lol(list):
    list_of_links = ""
    for item in list:
        list_of_links += '<li>\n<a href="{0[0]}">{0[1]}</a>\n'.format(item)
        if len(item) > 2 and str(item) != item:
            list_of_links += "<ul>\n"
            list_of_links += lol(item[2])
            list_of_links += "</ul>\n"
        list_of_links += "</li>\n"
    return list_of_links


@register.simple_tag
def iconize(type, size=32, set="crystal", default_type="application/octet-stream"):
    home = "http://www.stdicon.com"
    params = {
        "size": size,
        "default": "{0}/{1}/{2}".format(home, set, default_type),
    }
    return '<img src="{0}/{1}/{2}?{3}" alt="" />'.format(
        home, set, type, urlencode(params).replace("&", "&amp;")
    )


@register.simple_tag
def flatpage_link(url, additional_class=False):
    try:
        flatpage = FlatPage.objects.get(url="/" + url + "/")
        if additional_class:
            return '<a href="{0}" class="{1}"><span>{2}</span></a>'.format(
                flatpage.url, additional_class, flatpage.title
            )
        else:
            return '<a href="{0}">{1}</a>'.format(flatpage.url, flatpage.title)
    except ObjectDoesNotExist:
        return ""


# extract (value from a dict and assign it to a new variable)
def do_extract(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % tag_name
    m = re.search(r"([\.\w]+) (.*?) as (\w+)", arg)
    if m:
        dictionary, index, variable = m.groups()
    else:
        m = re.search(r"(.*?) (.*?)", arg)
        if m:
            dictionary, index = m.groups()
            variable = None
        else:
            raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return ExtractValue(dictionary, index, variable)


class ExtractValue(template.Node):
    def __init__(self, dictionary, index, variable):
        self.dictionary = template.Variable(dictionary)
        self.dict_name = dictionary
        self.index = index
        self.variable = variable

    def render(self, context):
        actual_dict = dict(self.dictionary.resolve(context))
        if actual_dict[context[self.index]]:
            value = actual_dict[context[self.index]]
        else:
            raise template.TemplateSyntaxError, "Context variable %s does not contain index %s!" % (
                self.dict_name,
                self.index,
            )
        if self.variable is not None:
            context[self.variable] = value
        else:
            return value


register.tag("extract", do_extract)

# memorize
def do_memorize(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % tag_name
    m = re.search(r"(.*?) as (\w+)", arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    var_value, var_name = m.groups()
    quotes = (
        '"',
        "'",
    )
    if var_value[0] in quotes:
        var_value = var_value[1:]
    if var_value[-1] in quotes:
        var_value = var_value[:-1]
    return ContextVariable(var_name, var_value)


class ContextVariable(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        context[self.var_name] = self.var_value
        return ""


register.tag("memorize", do_memorize)


# navigation tags for determining the current menu item


@register.simple_tag(takes_context=True)
def is_current(context, pattern, css=None, path=None):
    """
    Determines whether the current path is identical to the one passed in the `pattern` argument.
    If the `css` argument is set it will be returned in case of the match.
    """
    if path is None:
        path = context.get("request").path
    current = path == pattern
    if css is not None:
        return css if current else ""
    else:
        return current


@register.simple_tag(takes_context=True)
def is_current_parent(context, pattern, css=None, path=None):
    """
    Determines whether the current path begins the one passed in the `pattern` argument, which is useful when determining subpages.
    If the `css` argument is set it will be returned in case of the match.
    """
    if path is None:
        path = context.get("request").path
    current = re.match(pattern, path)
    if css is not None:
        return css if current else ""
    else:
        return current
