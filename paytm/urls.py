from django.urls import path
from .views import handleresponse

urlpatterns = [
		path('',handleresponse,name='handle'),
]