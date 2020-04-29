from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from website.models import Subscribe, ContactUs, PersonProfile, PersonChildren, PersonPhotos
from django.urls import reverse
# Create your views here.


def index(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		print(email)
		s = Subscribe()
		s.email = email
		s.save()
		return HttpResponseRedirect(reverse('website:home'))
	else:
		context = {}	
		context['person'] = list(PersonProfile.objects.all().values())
		return render(request, 'website/index.html', context)


def prifile(request, pid):
	context = {'pid': pid}
	person = list(PersonProfile.objects.filter(id=pid).values())[0]

	try:
		context['fathers_name'] = list(PersonProfile.objects.filter(id=person['fathers_name_id']).values())[0]['name']
	except Exception as e:
		pass

	try:
		context['mothers_name'] = list(PersonProfile.objects.filter(id=person['mothers_name_id']).values())[0]['name']
	except Exception as e:
		pass

	try:
		context['spouse_name'] = list(PersonProfile.objects.filter(id=person['spouse_name_id']).values())[0]['name']
	except Exception as e:
		pass


	try:
		children = list(PersonChildren.objects.filter(parent__id=person['id']).values())
		c = []
		for child in children:
			name = list(PersonProfile.objects.filter(id=child['child_id']).values())[0]['name']
			child_id = child['child_id']
			c.append({'id': child_id, 'name': name})

		context['children'] = c

	except Exception as e:
		pass


	try:
		context['pics'] = list(PersonPhotos.objects.filter(person__id=person['id']).values('pic'))
	except Exception as e:
		pass






	context['person'] = person
	return render(request, 'website/profile.html', context)

def about(request):
	return render(request, 'website/about.html')

def services(request):
	return render(request, 'website/services.html')

def contact(request):
	if request.method == 'POST':
		name = request.POST['name']
		subject = request.POST['subject']
		email = request.POST['email']
		message = request.POST['message']
		ContactUs.objects.create(name = name, email = email, subject = subject, message = message)
		context = {}
		context['sent'] = True
		return render(request, 'website/contact.html', context)

	return render(request, 'website/contact.html')

