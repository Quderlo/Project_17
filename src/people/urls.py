from django.urls import path

from people.views import PeopleCreateView

urlpatterns = [
    path('people-create/', PeopleCreateView.as_view(), name='people-create'),
]