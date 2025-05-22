from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Vehicle
from service.service.VehicleService import VehicleService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class VehicleCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'tid': 1, 'vehicleType': "Sedan"},
            {'tid': 2, 'vehicleType': "SUV"},
            {'tid': 3, 'vehicleType': "XUV"},
            {'tid': 4, 'vehicleType': "Pick-up"},
            {'tid': 5, 'vehicleType': "Hunchback"},
            {'tid': 6, 'vehicleType': "Sports"}
        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['vehicleId'] = requestForm["vehicleId"]
        self.form['vehicleName'] = requestForm['vehicleName']
        self.form['tid'] = requestForm["tid"]
        self.form['purchaseDate'] = requestForm["purchaseDate"]
        self.form['buyerName'] = requestForm["buyerName"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form["vehicleId"])):
            self.form["error"] = True
            inputError["vehicleId"] = "id can not be null"
        elif (DataValidator.max_len_20(self.form['vehicleId'])):
            inputError['vehicleId'] = "Id can should be below 20 digit"
            self.form['error'] = True
        elif (DataValidator.isnumb(self.form['vehicleId'])):
            inputError['vehicleId'] = "Incorrect ID,Id should be number"
            self.form['error'] = True
        else:
            if (DataValidator.is_0(self.form['vehicleId'])):
                inputError['vehicleId'] = "ID can not be 0 or less than 0"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['vehicleName'])):
            self.form["error"] = True
            inputError["vehicleName"] = "vehicleName can not be null"
        elif (DataValidator.max_len_50(self.form['vehicleName'])):
            inputError['vehicleName'] = "Name can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['vehicleName'])):
                inputError['vehicleName'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['tid'])):
            self.form["error"] = True
            inputError["tid"] = "Type can not be null"

        if DataValidator.isNull(self.form['purchaseDate']):
            inputError['purchaseDate'] = "purchase date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['purchaseDate']):
                inputError[
                    'purchaseDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['buyerName'])):
            self.form["error"] = True
            inputError["buyerName"] = "Buyer Name can not be null"
        elif (DataValidator.max_len_50(self.form['buyerName'])):
            inputError['buyerName'] = "Buyer Name can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['buyerName'])):
                inputError['buyerName'] = "Buyer Name contains only letters"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNotNull(self.form["vehicleId"])):
            if (DataValidator.max_len_20(self.form['vehicleId'])):
                inputError['vehicleId'] = "Id can should be below 20 digit"
                self.form['error'] = True
            # elif (DataValidator.isnumb(self.form['vehicleId'])):
            #     inputError['vehicleId'] = "Incorrect ID,Id should be number"
            #     self.form['error'] = True
            else:
                if (DataValidator.is_0(self.form['vehicleId'])):
                    inputError['vehicleId'] = "ID can not be 0 or less than 0"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['vehicleName'])):
            if (DataValidator.max_len_50(self.form['vehicleName'])):
                inputError['vehicleName'] = "Name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['vehicleName'])):
                    inputError['vehicleName'] = "Name contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['tid'])):
            pass

        if DataValidator.isNotNull(self.form['purchaseDate']):
            if DataValidator.isDate(self.form['purchaseDate']):
                inputError[
                    'purchaseDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form['buyerName'])):
            if (DataValidator.max_len_50(self.form['buyerName'])):
                inputError['buyerName'] = "Buyer Name can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['buyerName'])):
                    inputError['buyerName'] = "Buyer Name contains only letters"
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
            params["vehicleName"] = json_request.get("vehicleName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Vehicle.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        res = {}
        json_request = json.loads(request.body)
        json_request['id'] = 0
        json_request['tid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["vehicleName"] = json_request.get("vehicleName", None)
            params["vehicleId"] = json_request.get("vehicleId", None)
            params["vehicleType"] = json_request.get("vehicleType", None)
            params["purchaseDate"] = json_request.get("purchaseDate", None)
            params["buyerName"] = json_request.get("buyerName", None)
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
                res["LastId"] = Vehicle.objects.last().id
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

        index = self.find_dict_index(preload_list, 'tid', self.form['tid'])

        print("ORS API vehicle ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.vehicleId = self.form["vehicleId"]
        obj.vehicleName = self.form["vehicleName"]
        obj.vehicleType = preload_list[index]["vehicleType"]
        obj.purchaseDate = self.form["purchaseDate"]
        obj.buyerName = self.form["buyerName"]
        obj.tid = self.form["tid"]
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
                dup = Vehicle.objects.exclude(id=self.form['id']).filter(vehicleName=self.form["vehicleName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "vehicle Name already exists"
                else:
                    r = self.form_to_model(Vehicle())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Vehicle.objects.filter(vehicleName=self.form["vehicleName"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "vehicle Name already exists"
                else:
                    r = self.form_to_model(Vehicle())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of vehicle
    def get_service(self):
        return VehicleService()
