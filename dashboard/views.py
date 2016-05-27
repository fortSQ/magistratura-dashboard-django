from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.utils.dateparse import parse_date
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import UserProfile, Widget

def index(request):
	if request.user.is_authenticated():
		widget_list = Widget.objects.filter(user=request.user).order_by('position', '-create_date')
		return render(request, 'account/index.html', {'widget_list': widget_list})
	else:
		return redirect('/admin/login/?next=/')
		
def log_out(request):
	if request.user.is_authenticated():
		logout(request)
	return redirect('index')
	
def settings(request):
	response = request.user.userprofile.json()
	if request.method == 'POST':
		post = request.POST
		user = User.objects.get(username=request.user.username)
		user.first_name	= post['name']
		user.last_name	= post['surname']
		user.save()
		user_profile = user.userprofile
		user_profile.birthday	= parse_date(post['birthdate'])
		user_profile.sex		= post['sex']
		user_profile.city		= post['city']
		user_profile.save()
		response = user_profile.json()
	return JsonResponse(response)
	
def widget(request):
	if request.method == 'GET':
		widgetId = request.GET.get('id')
		widget = get_object_or_404(Widget, pk=widgetId)
		return JsonResponse(widget.json())
	elif request.method == 'PUT':
		widget = Widget()
		widget = set_widget_fields_from_request(widget, request)
		widget.user = request.user
		widget.save()
		return render(request, 'widget/item.html', {'widget': widget})
	elif request.method == 'POST':
		widgetId = request.POST.get('id')
		widget = get_object_or_404(Widget, pk=widgetId, user=request.user)
		widget = set_widget_fields_from_request(widget, request)
		widget.publish()
		return JsonResponse(widget.json())
	elif request.method == 'DELETE':
		widgetId = QueryDict(request.body).get('id')
		Widget.objects.get(pk=widgetId, user=request.user).delete()
		return JsonResponse({'id': widgetId})
		
def set_widget_fields_from_request(widget, request):
	body = QueryDict(request.body)
	if body.get('image'):
		widget.image = body.get('image')
	if body.get('color'):
		widget.color = body.get('color')
	if body.get('message'):
		widget.message = body.get('message')
	return widget

def widget_sort(request):
	sortIdList = request.POST.getlist('sort[]')
	for (position, widgetId) in enumerate(sortIdList):
		widget = get_object_or_404(Widget, pk=widgetId, user=request.user)
		widget.position = position + 1
		widget.save()
	return JsonResponse({'status': 'ok'})
	
def user_dashboard(request, login):
	if not request.user.is_authenticated():
		return redirect('index')
	user = get_object_or_404(User, username=login)
	widget_list = Widget.objects.filter(user=user).order_by('position', '-create_date')
	return render(request, 'account/index.html', {'widget_list': widget_list})