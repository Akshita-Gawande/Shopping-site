from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^products$', views.products, name='products'),
    url(r'^cart$', views.cart_products, name='cart_products')
    #url(r'^home/$', views.simple_upload, name='simple_upload'),
]
