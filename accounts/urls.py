from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(
        '^login/$',
        auth_views.login,
        {'redirect_authenticated_user': 'BotTelegram:index'},
        name='login',
    ),
    #url('^', include('django.contrib.auth.urls')),
    #url('^', include('django.contrib.auth.urls')),
    #url('^crear/$',views.crear_cuenta,name="crear_cuenta")
]
