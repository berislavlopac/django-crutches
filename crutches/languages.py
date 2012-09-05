# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.simple import redirect_to
from django.utils.translation import activate, check_for_language, get_language

LANGUAGE_LIST        = [x for (x, y) in settings.LANGUAGES]
LANGUAGE_DEFAULT     = LANGUAGE_LIST[0]

def languages(view):
    """ Checks whether the language was set in the URL and sets it if so. """
    def wrapper(request, *args, **kw):
        get = request.GET.copy()
        lang = get.pop('lang', None)
        if lang:
            set_language(request, lang[0])
            return redirect_to(request, url=request.path+'?'+get.urlencode(), permanent=False, query_string=False)
        return view(request, *args, **kw)
    return wrapper

def set_language(request, lang_code):
    if lang_code in LANGUAGE_LIST:
        if hasattr(request, 'session'):
            request.session['django_language'] = lang_code
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        activate(lang_code)
    else:
        set_language(request, LANGUAGE_DEFAULT)

def asciify(string):
    #table_raw =  {
    #    u'Š':u'S', u'š':u's', u'Đ':u'Dj', u'đ':u'dj', u'Ž':u'Z', u'ž':u'z', u'Č':u'C', u'č':u'c', u'Ć':u'C', u'ć':u'c',
    #    u'À':u'A', u'Á':u'A', u'Â':u'A', u'Ã':u'A', u'Ä':u'A', u'Å':u'A', u'Æ':u'A', u'Ç':u'C', u'È':u'E', u'É':u'E',
    #    u'Ê':u'E', u'Ë':u'E', u'Ì':u'I', u'Í':u'I', u'Î':u'I', u'Ï':u'I', u'Ñ':u'N', u'Ò':u'O', u'Ó':u'O', u'Ô':u'O',
    #    u'Õ':u'O', u'Ö':u'O', u'Ø':u'O', u'Ù':u'U', u'Ú':u'U', u'Û':u'U', u'Ü':u'U', u'Ý':u'Y', u'Þ':u'B', u'ß':u'Ss',
    #    u'à':u'a', u'á':u'a', u'â':u'a', u'ã':u'a', u'ä':u'a', u'å':u'a', u'æ':u'a', u'ç':u'c', u'è':u'e', u'é':u'e',
    #    u'ê':u'e', u'ë':u'e', u'ì':u'i', u'í':u'i', u'î':u'i', u'ï':u'i', u'ð':u'o', u'ñ':u'n', u'ò':u'o', u'ó':u'o',
    #    u'ô':u'o', u'õ':u'o', u'ö':u'o', u'ø':u'o', u'ù':u'u', u'ú':u'u', u'û':u'u', u'ý':u'y', u'ý':u'y', u'þ':u'b',
    #    u'ÿ':u'y', u'Ŕ':u'R', u'ŕ':u'r',
    #}
    table =  {
        ord(u'Š'):u'S', ord(u'š'):u's', ord(u'Đ'):u'Dj', ord(u'đ'):u'dj', ord(u'Ž'):u'Z', ord(u'ž'):u'z', ord(u'Č'):u'C', ord(u'č'):u'c', ord(u'Ć'):u'C', ord(u'ć'):u'c',
        ord(u'À'):u'A', ord(u'Á'):u'A', ord(u'Â'):u'A', ord(u'Ã'):u'A', ord(u'Ä'):u'A', ord(u'Å'):u'A', ord(u'Æ'):u'A', ord(u'Ç'):u'C', ord(u'È'):u'E', ord(u'É'):u'E',
        ord(u'Ê'):u'E', ord(u'Ë'):u'E', ord(u'Ì'):u'I', ord(u'Í'):u'I', ord(u'Î'):u'I', ord(u'Ï'):u'I', ord(u'Ñ'):u'N', ord(u'Ò'):u'O', ord(u'Ó'):u'O', ord(u'Ô'):u'O',
        ord(u'Õ'):u'O', ord(u'Ö'):u'O', ord(u'Ø'):u'O', ord(u'Ù'):u'U', ord(u'Ú'):u'U', ord(u'Û'):u'U', ord(u'Ü'):u'U', ord(u'Ý'):u'Y', ord(u'Þ'):u'B', ord(u'ß'):u'Ss',
        ord(u'à'):u'a', ord(u'á'):u'a', ord(u'â'):u'a', ord(u'ã'):u'a', ord(u'ä'):u'a', ord(u'å'):u'a', ord(u'æ'):u'a', ord(u'ç'):u'c', ord(u'è'):u'e', ord(u'é'):u'e',
        ord(u'ê'):u'e', ord(u'ë'):u'e', ord(u'ì'):u'i', ord(u'í'):u'i', ord(u'î'):u'i', ord(u'ï'):u'i', ord(u'ð'):u'o', ord(u'ñ'):u'n', ord(u'ò'):u'o', ord(u'ó'):u'o',
        ord(u'ô'):u'o', ord(u'õ'):u'o', ord(u'ö'):u'o', ord(u'ø'):u'o', ord(u'ù'):u'u', ord(u'ú'):u'u', ord(u'û'):u'u', ord(u'ý'):u'y', ord(u'ý'):u'y', ord(u'þ'):u'b',
        ord(u'ÿ'):u'y', ord(u'Ŕ'):u'R', ord(u'ŕ'):u'r',
    }
    return string.translate(table)
