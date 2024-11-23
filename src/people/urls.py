from django.urls import path

from people.views import PeopleCreateView, PeopleListView, PeopleDetailView

urlpatterns = [
    path('person-list/', PeopleListView.as_view(), name='person-list'),
    path('person-create/', PeopleCreateView.as_view(), name='person-create'),
    path('person/detail/<int:pk>/', PeopleDetailView.as_view(), name='person-detail'),
]