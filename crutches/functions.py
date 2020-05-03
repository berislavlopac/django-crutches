# -*- coding: utf-8 -*-

import string
from random import choice
from datetime import date, timedelta
from django.template import *
from django.shortcuts import render_to_response
from django.utils.functional import lazy
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


def order(val1, val2):
    """Returns an ordered pair (tuple) with the larger argument first."""
    if val1 >= val2:
        return (val1, val2)
    else:
        return (val2, val1)


def slugify_filename(filename):
    """Makes sure that the extension is preserved when slugifying a filename."""
    name, dot, extension = filename.rpartition(u".")
    return u".".join((slugify(name), extension))


def shift_months(months_to_add, basedate=None):
    """ Moves a date a fixed number of months. Pass a negative number to move backwards in time. """
    if basedate is None:
        basedate = date.today()
    years_to_add, month = divmod(basedate.month + months_to_add, 12)
    if month == 0:
        month = 12
    return date(basedate.year + years_to_add, month, 1) + timedelta(
        days=basedate.day - 1
    )


def render_to(template):
    """ Allows views to return dict and render appropriate templates."""

    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            return render_to_response(
                template, output, context_instance=RequestContext(request)
            )

        return wrapper

    return renderer


def get_age(birthday, format="y"):
    """ Returns "age" since the given "birthday", in days (format='d'), months (format='m') or years (any other format). """
    today = date.today()
    if format.lower() in ("d", "days"):
        return (today - birthday).days
    years = today.year - birthday.year
    birthday_this_year = date(today.year, birthday.month, birthday.day)
    if birthday_this_year > today:
        years = years - 1
    if format.lower() in ("m", "months"):
        return years * 12 + today.month - birthday_this_year.month
    return years


def attribs(object, as_unicode=False):
    """ Returns all object attributes as a dict. """
    return dict(
        (key, unicode(value) if as_unicode else value)
        for key, value in object.__dict__.iteritems()
        if not callable(value) and not key.startswith("__")
    )


def create_model(
    name, fields=None, app_label="", module="", options=None, admin_opts=None
):
    """ Create specified model. """

    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, "app_label", app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {"__module__": module, "Meta": Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:

        class Admin(admin.ModelAdmin):
            pass

        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)
    return model


def int_str(
    number,
    base=None,
    digits="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
):
    """ Converts a number to its string representation. """
    if base is None:
        base = len(digits)
    if number != long(number):
        raise TypeError, "The number must be an integer (or long integer)."
    if base < 2 or base > len(digits):
        raise NotImplementedError, "The base must be between 2 and {0}.".format(
            len(digits)
        )
    # for numbers smaller than the base
    if number <= base:
        return digits[number]
    # for all other cases
    result = []
    while number:
        rem = number % base
        number = number // base
        result.insert(0, digits[rem])
    return "".join(result)


def int_base(
    source,
    base=None,
    digits="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
):
    """ The equivalent to int(), but the base may go up to 62 (allowing for uppercase letters). """
    if base is None:
        base = len(digits)
    if base < 2 or base > 62:
        raise NotImplementedError, "int_base() base must be >= 2 and <= {0}.".format(
            len(digits)
        )
    result = 0
    step = len(source)
    for char in source:
        step = step - 1
        value = digits.index(char, 0, base) * base ** step
        result += value
    return result


def base_convert(source, base_from, base_to):
    """ Returns a string containing number represented in base tobase.
        The equivalent to PHP's base_convert, but the base may go up to 62 (allowing for uppercase letters). """
    return int_str(int_base(source, base_from), base_to)


def reverse_lazy(name=None, *args, **kwargs):
    return lazy(reverse, str)(name, args=args, kwargs=kwargs)


def random_string(length=8, chars=string.letters + string.digits):
    """ Returns a string of `length` characters randomly selected out of `chars`. Appropriate for passwords and other random strings. """
    return "".join([choice(chars) for i in range(length)])


def naturallysorted(L, reverse=False):
    """ Similar functionality to sorted() except it does a natural text sort
    which is what humans expect when they see a filename list.
    Originally developed by Peter Nixon: http://peternixon.net/news/2009/07/28/natural-text-sorting-in-python/
    """
    convert = lambda text: ("", int(text)) if text.isdigit() else (text, 0)
    alphanum = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(L, key=alphanum, reverse=reverse)


# end
