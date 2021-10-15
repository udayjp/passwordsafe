from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('api/signup/',UserRegistrationView.as_view(),name='user_registration'),
    path('api/record/',RecordListCreateAPIView.as_view(),name='list_create_record'),
    url(r'^api/record/(?P<pk>\d+)', update_delete_record, name='update_delete_record'),
]