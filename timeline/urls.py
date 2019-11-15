
from django.conf.urls import url, include
from timeline.forms import LoginForm

from . import views


urlpatterns = [
	url(r'^$', views.mainpage, name='mainpage'),
    url(r'staff$', views.staffsite, name='staffsite'),
    url(r'delete$', views.staffsite),
    url(r'approve$', views.staffsite),
    url(r'profile$', views.profile, name='profile'),
    ]