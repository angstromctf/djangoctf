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
        tree = "<li><a href=\"" + reverse('learn:module', args=[module.name]) + "\">" + module.title + "</a></li>"

        if module.first_child is not None:
            tree += "<ul>" + gen_tree(module.first_child) + "</ul>"

        if module.next is not None:
            tree += gen_tree(module.next)

        return tree


    return mark_safe("<ul>" + gen_tree(module) + "</ul>")