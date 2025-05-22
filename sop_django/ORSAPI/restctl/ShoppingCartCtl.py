from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import ShoppingCart
from service.service.ShoppingCartService import ShoppingCartService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class ShoppingCartCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'pid': 1, 'product': "Mobile"},
            {'pid': 2, 'product': "Tablet"},
            {'pid': 3, 'product': "Charger"},
            {'pid': 4, 'product': "Laptop"},
            {'pid': 5, 'product': "Earbuds"},
            {'pid': 6, 'product': "Neckband"}
        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['name'] = requestForm["name"]
        self.form['pid'] = requestForm["pid"]
        self.form['date'] = requestForm["date"]
        self.form['quantity'] = requestForm["quantity"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['name'])):
            self.form["error"] = True
            inputError["name"] = "Name can not be null"
        elif (DataValidator.max_len_50(self.form['name'])):
            inputError['name'] = "Name can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['pid'])):
            self.form["error"] = True
            inputError["pid"] = "Product can not be null"

        if DataValidator.isNull(self.form['date']):
            inputError['date'] = "Date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['date']):
                inputError[
                    'date'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["quantity"])):
            self.form["error"] = True
            inputError["quantity"] = "quantity can not be null"
        elif (DataValidator.max_len_20(self.form['quantity'])):
            inputError['quantity'] = "quantity can should be below 20 digit"
            self.form['error'] = True
        elif (DataValidator.isnumb(self.form['quantity'])):
            inputError['quantity'] = "Incorrect,quantity should be number"
            self.form['error'] = True
        else:
            if (DataValidator.is_0(self.form['quantity'])):
                inputError['quantity'] = "quantity can not be 0 or less than 0"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form['name'])):
            if (DataValidator.max_len_50(self.form['name'])):
                inputError['name'] = "Name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['name'])):
                    inputError['name'] = "Name contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['pid'])):
            pass

        if DataValidator.isNotNull(self.form['date']):
            if DataValidator.isDate(self.form['date']):
                inputError[
                    'date'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form["quantity"])):
            if (DataValidator.max_len_20(self.form['quantity'])):
                inputError['quantity'] = "quantity can should be below 20 digit"
                self.form['error'] = True
            elif (DataValidator.isnumb(self.form['quantity'])):
                inputError['quantity'] = "Incorrect, quantity should be number"
                self.form['error'] = True
            else:
                if (DataValidator.is_0(self.form['quantity'])):
                    inputError['quantity'] = "quantity can not be 0 or less than 0"
                    self.form['error'] = True

        return self.form["error"]

    def get(self, request, params={}):
        c = self.get_service().get(params['id'])
        res = {}
        if (c != None):
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data found"
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data": res["data"]})

    def delete(self, request, params={}):
        c = self.get_service().get(params["id"])
        res = {}
        if (c != None):
            self.get_service().delete(params["id"])
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data has been deleted Successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data": res})

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["name"] = json_request.get("name", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = ShoppingCart.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        res = {}
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['pid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["name"] = json_request.get("name", None)
            params["pid"] = json_request.get("pid", None)
            params["date"] = json_request.get("date", None)
            params["quantity"] = json_request.get("quantity", None)
            params["pageNo"] = json_request.get("pageNo", None)
        self.request_to_form(json_request)
        if (self.input_validation1()):
            print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            res["error"] = True
            res["mesg"] = "No record found"
        else:
            c = self.get_service().search1(params)
            # res = {"mesg": ""}
            if (c != None):
                res["data"] = c["data"]
                if res["data"] == []:
                    res["mesg"] = "No record found"
                res["MaxId"] = c["MaxId"]
                res["index"] = c["index"]
                res["LastId"] = ShoppingCart.objects.last().id
                res["error"] = False
            else:
                res["error"] = True
                res["message"] = "No record found"
        return JsonResponse({"result": res, "form": self.form})

    def find_dict_index(self, dict_list, key, value):
        for index, item in enumerate(dict_list):
            if int(item.get(key)) == int(value):
                print('--------------', index)
                return index

    def form_to_model(self, obj):
        preload_response = self.preload(None).content.decode()
        preload_data = json.loads(preload_response)
        preload_list = preload_data["preloadList"]

        index = self.find_dict_index(preload_list, 'pid', self.form['pid'])

        print("ORS API ShoppingCart ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.product = preload_list[index]["product"]
        obj.date = self.form["date"]
        obj.quantity = self.form["quantity"]
        obj.pid = self.form["pid"]
        return obj

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (self.form["id"] > 0):
                dup = ShoppingCart.objects.exclude(id=self.form['id']).filter(name=self.form["name"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Name already exists"
                else:
                    r = self.form_to_model(ShoppingCart())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = ShoppingCart.objects.filter(name=self.form["name"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Name already exists"
                else:
                    r = self.form_to_model(ShoppingCart())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of ShoppingCart
    def get_service(self):
        return ShoppingCartService()
