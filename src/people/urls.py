from django.urls import path

from people.views import PeopleCreateView, PeopleListView, PeopleDetailView

urlpatterns = [
    path('people-list/', PeopleListView.as_view(), name='people-list'),
    path('people-create/', PeopleCreateView.as_view(), name='people-create'),
    path('people/detail/<int:pk>/', PeopleDetailView.as_view(), name='people-detail'),
]