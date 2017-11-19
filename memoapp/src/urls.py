from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create-memo$', views.create_memo),
    url(r'^history$', views.history),
    url(r'^get-memo/(\d+)$', views.get_memo),
    url(r'^search$', views.search_page),
    url(r'^search-notes$', views.search),
]
