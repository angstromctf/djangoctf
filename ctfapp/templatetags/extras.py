from django import template

register = template.Library()

@register.filter
def is_solved(problem, solved):
	return (problem.id in solved) and solved[problem.id][0]

@register.filter
def try_count(problem, solved):
	return solved[problem.id][1] if problem.id in solved else 1