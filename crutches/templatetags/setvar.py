# -*- coding: utf-8 -*-

from django import template

register = template.Library()

class SetVariable(template.Node):
    def __init__(self, varname, nodelist):
        self.varname = varname
        self.nodelist = nodelist

    def render(self,context):
        context[self.varname] = self.nodelist.render(context)
        return ''

@register.tag(name='setvar')
def setvar(parser, token):
    """
    Set value to content of a rendered block.
    {% setvar var_name %}
     ....
    {% endsetvar %}
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument for variable name" % token.contents.split()[0]

    nodelist = parser.parse(('endsetvar',))
    parser.delete_first_token()
    return SetVariable(varname, nodelist)