from django.urls import path

from . import views

urlpatterns = [
    path('', views.confirmation.as_view(), name='confirmation'),
    path('thanks', views.thanks, name='thanks'), 
]