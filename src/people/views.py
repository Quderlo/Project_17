from django.shortcuts import render
from django.views import View


# Create your views here.
class PeopleCreateView(View):
    def get(self, request):
        return render(
            request,
            'people/people-create.html',
        )