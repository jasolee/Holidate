
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from timeline.forms import LoginForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('timeline.urls')),
    url(r'^logout/$', views.logout, {'next_page': '/Login/'}), 
    url(r'^Login/$', views.login,{'template_name': 'mysite_login/cool_login.html', 'authentication_form': LoginForm}, name='login'),
]
