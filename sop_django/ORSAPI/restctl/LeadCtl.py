from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Lead
from service.service.LeadService import LeadService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class LeadCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'sid': 1, 'status': "Hot"},
            {'sid': 2, 'status': "Cold"},
            {'sid': 3, 'status': "Warm"}
        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['date'] = requestForm["date"]
        self.form['contactName'] = requestForm["contactName"]
        self.form['mobile'] = requestForm["mobile"]
        self.form['sid'] = requestForm["sid"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form['contactName'])):
            self.form["error"] = True
            inputError["contactName"] = "contactName can not be null"
        elif (DataValidator.max_len_50(self.form['contactName'])):
            inputError['contactName'] = "contactName can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['contactName'])):
                inputError['contactName'] = "contactName contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['sid'])):
            self.form["error"] = True
            inputError["sid"] = "status can not be null"

        if DataValidator.isNull(self.form['date']):
            inputError['date'] = "mobile can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['date']):
                inputError['date'] = "Incorrect date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["mobile"])):
            inputError["mobile"] = "Mobile No. can not be null"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form["mobile"])):
            if (DataValidator.ismobilecheck(self.form['mobile'])):
                self.form["error"] = True
                inputError["mobile"] = "Enter Correct Mobile No.,and it should be started form 6-9"

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form['contactName'])):
            if (DataValidator.max_len_50(self.form['contactName'])):
                inputError['contactName'] = "contactName can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['contactName'])):
                    inputError['contactName'] = "contactName contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['sid'])):
            pass

        if DataValidator.isNotNull(self.form['date']):
            if DataValidator.isDate(self.form['date']):
                inputError['date'] = "Incorrect date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form["mobile"])):
            if (DataValidator.ismobilecheck(self.form['mobile'])):
                self.form["error"] = True
                inputError["mobile"] = "Enter Correct Mobile No.,and it should be started form 6-9"
            else:
                if (DataValidator.max_len_10(self.form['mobile'])):
                    inputError['contactName'] = "mobile no. should be of 10 character"
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
            params["contactName"] = json_request.get("contactName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Lead.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        res = {}
        json_request = json.loads(request.body)
        json_request['id'] = 0
        # json_request['contactName'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["date"] = json_request.get("date", None)
            params["contactName"] = json_request.get("contactName", None)
            params["mobile"] = json_request.get("mobile", None)
            params["sid"] = json_request.get("sid", None)
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
                res["LastId"] = Lead.objects.last().id
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

        index = self.find_dict_index(preload_list, 'sid', self.form['sid'])

        print("ORS API Lead ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.date = self.form["date"]
        obj.status = preload_list[index]["status"]
        obj.mobile = self.form["mobile"]
        obj.sid = self.form["sid"]
        obj.contactName = self.form["contactName"]
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
                dup = Lead.objects.exclude(id=self.form['id']).filter(contactName=self.form["contactName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "contactName already exists"
                else:
                    r = self.form_to_model(Lead())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Lead.objects.filter(contactName=self.form["contactName"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "contactName already exists"
                else:
                    r = self.form_to_model(Lead())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Lead
    def get_service(self):
        return LeadService()
