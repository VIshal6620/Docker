from django.shortcuts import render
from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from ORS.utility.HtmlUtility import HTMLUtility
from service.models import Favorite
from service.service.FavoriteService import FavoriteService


class FavoriteCtl(BaseCtl):

    def preload(self, request, params):

        self.form["product"] = request.POST.get('product', '')

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["product"] = obj.product

        self.static_preload = {"laptop": "laptop", "phone": "phone","Tablet": "Tablet"}

        self.form["preload"]["product"] = HTMLUtility.get_list_from_dict(
            'product',
            self.form["product"],
            self.static_preload
        )

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['product'] = requestForm['product']
        self.form['addedDate'] = requestForm['addedDate']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.product = self.form['product']
        obj.addedDate = self.form['addedDate']
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return obj
        self.form['id'] = obj.id
        self.form['product'] = obj.product
        self.form['addedDate'] = obj.addedDate

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['product'])):
            inputError['product'] = "product is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['product'])):
                inputError['product'] = "product is contain"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['addedDate'])):
            inputError['addedDate'] = "addedDate is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['addedDate'])):
                inputError['addedDate'] = "addedDate is YYYY-MM-DD Contain"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Favorite())
        self.get_service().save(r)
        self.form['messege'] = "Data saved successfully"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Favorite.html"

    def get_service(self):
        return FavoriteService()
