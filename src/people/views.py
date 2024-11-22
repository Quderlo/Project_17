from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from people.models import Person


class PeopleListView(ListView):
    model = Person
    context_object_name = "persons"
    template_name = "people/people-list.html"


# Create your views here.
class PeopleCreateView(View):
    def get(self, request):
        return render(
            request,
            'people/people-create.html',
        )

class PeopleDetailView(DetailView):
    model = Person
    template_name = "people/people-detail.html"