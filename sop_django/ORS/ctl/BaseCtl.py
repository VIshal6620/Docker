from django.http import HttpResponse
from abc import ABC, abstractmethod
from django.shortcuts import render, redirect

'''
Base class is inherited by all application controllers
'''

class BaseCtl(ABC):
    #contains static and dynamic preload data
    static_preload = {}
    dynamic_preload = {}


    # Contains list of objects, it will be displayed at list page
    page_list = {}

    '''
    Initialize controller attributes
    '''

    def __init__(self):
        self.form = {}
        self.form["id"] = 0
        self.form["message"] = ""
        self.form["error"] = False
        self.form["inputError"] = {}
        self.form["pageNo"] = 1
        self.form["preload"] = {}

    '''
    It loads preload data of the page
    '''

    def preload(self, request,id):
        pass

    '''
    execute method is executed for each HTTP request.
    It inturn calls display() or submit() method for HTTP GET and HTTP POST methods 
    '''

    def execute(self, request, params={}):
        print("This is execute")
        self.preload(request,params)
        if "GET" == request.method:
            return self.display(request, params)
        elif "POST" == request.method:
            self.request_to_form(request.POST)
            if self.input_validation():
                return self.display(request,params)
            else:
                if (request.POST.get("operation") == "Delete"):
                    return self.deleteRecord(request, params)
                elif (request.POST.get("operation") == "next"):
                    return self.next(request, params)
                elif (request.POST.get("operation") == "previous"):
                    return self.previous(request, params)

                else:
                    return self.submit(request, params)
        else:
            message = "Request is not supported"
            return HttpResponse(message)

    def deleteRecord(self, request, params={}):
        pass

    '''
    delete record of received ID
    '''

    @abstractmethod
    def display(self, request, params={}):
        pass

    '''
    submit data
    '''

    @abstractmethod
    def submit(self, request, params={}):
        pass

    '''
    Populate values from Request POST/GET to Controller form object 
    '''

    def request_to_form(self, requestForm):
        pass

    # Populate Form from Model

    def model_to_form(self, obj):
        pass

    # Convert form into module
    def form_to_model(self, obj):
        pass

    '''
    Apply input validation
    '''

    def input_validation(self):
        self.form["error"] = False
        self.form["message"] = ""

    '''
    Returns template of Controller
    '''

    @abstractmethod
    def get_template(self):
        pass

    @abstractmethod
    def get_service(self):
        pass
