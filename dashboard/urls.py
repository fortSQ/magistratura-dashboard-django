from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^logout', views.log_out, name='log_out'),
	url(r'^settings', views.settings, name='settings'),
	url(r'^widget$', views.widget, name='widget'),
	url(r'^widget/sort', views.widget_sort, name='widget_sort'),
	url(r'^user/(?P<login>[\w]+)$', views.user_dashboard, name='user_dashboard'),
]