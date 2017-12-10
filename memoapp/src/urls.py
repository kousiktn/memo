from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create-memo$', views.create_memo),
    url(r'^history$', views.history),
    url(r'^get-memo/$', views.get_memo),
]
