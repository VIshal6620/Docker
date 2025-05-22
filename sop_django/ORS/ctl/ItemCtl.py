from datetime import datetime

from django.shortcuts import render

from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from ORS.utility.HtmlUtility import HTMLUtility
from service.models import Item
from service.service.ItemService import ItemService


class ItemCtl(BaseCtl):
    def preload(self, request, params):

        self.form["category"] = request.POST.get('category', '')


        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["category"] = obj.category

        self.static_preload = {"Developer": "Developer", "NonDeveloper": "NonDeveloper"}


        self.form["preload"]["category"] = HTMLUtility.get_list_from_dict(
            'category',
            self.form["category"],
            self.static_preload
        )

    # Polulate Form from Http request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["title"] = requestForm["title"]
        self.form["overview"] = requestForm["overview"]
        self.form["cost"] = requestForm["cost"]
        self.form["purchaseDate"] = requestForm["purchaseDate"]



    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["title"] = obj.title
        self.form["overview"] = obj.overview
        self.form["cost"] = obj.cost
        self.form["purchaseDate"] = obj.purchaseDate


    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.title = self.form["title"]
        obj.overview = self.form["overview"]
        obj.cost = self.form["cost"]
        obj.purchaseDate = self.form["purchaseDate"]
        return obj

    # Validate form

    def input_validation(self):
        super ().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["title"])):
            inputError["title"] = " Name can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["overview"])):
            inputError["overview"] = " overview Name can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["cost"].strip())):
            inputError["cost"] = " cost can not be null"
            self.form["error"] = True


        if (DataValidator.isNull(self.form["purchaseDate"])):
            inputError["purchaseDate"] = "purchaseDate can not be null"
            self.form["error"] = True


        return self.form['error']

        # Display User Page

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Item())
        self.get_service().save(r)
        self.form['messege'] = "Data Successfully Saved"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Item.html"

    def get_service(self):
        return ItemService()

