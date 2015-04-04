from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .models import Problem
from .forms import SubmitForm, LoginForm

import hashlib

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

#@login_required
def problems(request):
	last_submission = -1
	good = False
	
	if request.method == 'POST':
		form = SubmitForm(request.POST)

		if form.is_valid():
			guess = form.cleaned_data["flag_guess"]
			pid = form.cleaned_data["problem"]
			last_submission = pid
			
			problem = Problem.objects.get(id=pid)
			good = hashlib.sha512(guess.encode()).hexdigest() == problem.flag_sha512_hash
		
	problem_list = Problem.objects.all()
	template = loader.get_template('problems.html')
	context = RequestContext(request, {
		'problem_list': problem_list,
		'form': SubmitForm(),
		'last': last_submission,
		'good': good,
	})
	return HttpResponse(template.render(context))

def login_view(request):
	template = loader.get_template('login.html')
	context = RequestContext(request, {
		'form': LoginForm(),
	})
	return HttpResponse(template.render(context))