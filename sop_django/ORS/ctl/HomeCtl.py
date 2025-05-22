
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render

class HomeCtl(BaseCtl):

    def display(self, request, params={}):
        print('--------------------------')
        return render(request, self.get_template())

    def submit(self, request, params={}):
        pass

    # Template html of role page
    def get_template(self):
        return "Home.html"

   # Service of Role
    def get_service(self):
        return "RoleService()"




