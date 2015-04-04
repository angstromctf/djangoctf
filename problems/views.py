from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Problem

def index(request):
    problem_list = Problem.objects.all()
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'problem_list': problem_list,
    })
    return HttpResponse(template.render(context))
