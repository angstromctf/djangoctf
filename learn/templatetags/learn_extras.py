from django import template
from django.contrib.humanize.templatetags.humanize import ordinal

from core.models import Team, ProblemUpdate
from core.utils.time import before_start
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def module_tree(context, module):
    def gen_tree(module):
        tree = "<li><a href=\"" + reverse('learn:module', args=[module.name]) + "\"" + (" id=\"active\"" if module == context['module'] else "") + ">" + module.title + "</a>"

        if module.first_child is not None:
            tree += "<ol>" + gen_tree(module.first_child) + "</ol>"

        tree += "</li>"

        if module.next is not None:
            tree += gen_tree(module.next)

        return tree

    return mark_safe("<ol>" + gen_tree(module) + "</ol>")


@register.simple_tag
def module_breadcrumbs(module):
    crumbs = ""
    current = module

    while current != None:
        crumbs = crumbs + "<li" + (" class=\"active\"" if current == module else "") + "><a href=\"" + reverse('learn:module', args=[current.name]) + "\">" + current.title + "</a></li>"
        current = current.parent

    return mark_safe(crumbs)