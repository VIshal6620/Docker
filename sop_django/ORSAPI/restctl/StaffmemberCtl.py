from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Staffmember
from service.service.StaffmemberService import StaffmemberService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class StaffmemberCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'did': 1, 'division': 'Devision A'},
            {'did': 2, 'division': 'Devision B'},
            {'did': 3, 'division': 'Devision C'},
            {'did': 4, 'division': 'Devision D'},
            {'did': 5, 'division': 'Devision E'},
            {'did': 6, 'division': 'Devision F'},
        ]
        return JsonResponse({"preloadList": preloadList})

    

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['fullName'] = requestForm["fullName"]
        self.form['joiningDate'] = requestForm["joiningDate"]
        self.form['did'] = requestForm["did"]
        self.form['previousEmployer'] = requestForm["previousEmployer"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form['joiningDate']):
            inputError['joiningDate'] = "joiningDate  can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['joiningDate']):
                inputError['joiningDate'] = "Incorrect Date  format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['fullName'])):
            self.form["error"] = True
            inputError["fullName"] = "fullName can not be null"
        elif (DataValidator.max_len_20(self.form['fullName'])):
            inputError['fullName'] = "fullName can should be below 20 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['fullName'])):
                inputError['fullName'] = "fullName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['previousEmployer'])):
            self.form["error"] = True
            inputError["previousEmployer"] = "previousEmployer can not be null"
        elif (DataValidator.max_len_20(self.form['previousEmployer'])):
            inputError['previousEmployer'] = "previousEmployer can should be below 20 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['previousEmployer'])):
                inputError['previousEmployer'] = "previousEmployer contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['did'])):
            self.form["error"] = True
            inputError["did"] = "Assign To can not be null"






        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if DataValidator.isNotNull(self.form['joiningDate']):
            if DataValidator.isDate(self.form['joiningDate']):
                inputError['joiningDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form['fullName'])):
            if (DataValidator.max_len_20(self.form['fullName'])):
                inputError['fullName'] = "fullName can should be below 20 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['fullName'])):
                    inputError['fullName'] = "fullName contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['previousEmployer'])):
            if (DataValidator.max_len_20(self.form['previousEmployer'])):
                inputError['previousEmployer'] = "previousEmployer can should be below 20 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['previousEmployer'])):
                    inputError['previousEmployer'] = "previousEmployer contains only letters"
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
            params["fullName"] = json_request.get("fullName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Staffmember.objects.last().id
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
            params["fullName"] = json_request.get("fullName", None)
            params["joiningDate"] = json_request.get("joiningDate", None)
            params["did"] = json_request.get("did", None)
            params["previousEmployer"] = json_request.get("previousEmployer", None)
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
                res["LastId"] = Staffmember.objects.last().id
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


        index = self.find_dict_index(preload_list, 'did', self.form['did'])


        print("ORS API Staffmember ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.fullName = self.form["fullName"]
        obj.joiningDate = self.form["joiningDate"]
        obj.previousEmployer = self.form["previousEmployer"]
        obj.division = preload_list[index]['division']
        obj.did = self.form["did"]
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
                dup = Staffmember.objects.exclude(id=self.form['id']).filter(fullName=self.form["fullName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Name already exists"
                else:
                    r = self.form_to_model(Staffmember())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Staffmember.objects.filter(fullName=self.form["fullName"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Name already exists"
                else:
                    r = self.form_to_model(Staffmember())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Staffmember
    def get_service(self):
        return StaffmemberService()
