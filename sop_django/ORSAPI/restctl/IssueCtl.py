from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Issue
from service.service.IssueService import IssueService
from service.service.UserService import UserService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class IssueCtl(BaseCtl):

    def preload(self, request,params={}):
        userList = UserService().preload()
        preloadList = []
        for x in userList:
            preloadList.append(x.to_json())
        return JsonResponse({"preloadList":preloadList})

    def preload1(self, request, params={}):
        preloadList =[
            {'sid': 1, 'status':'Open'},
            {'sid': 2, 'status':'In Progress'},
            {'sid': 3, 'status':'Hold'},
            {'sid': 4, 'status':'Resolve'},
            {'sid': 5, 'status':'Close'}

        ]
        return JsonResponse({"preloadList1": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['openDate'] = requestForm["openDate"]
        self.form['title'] = requestForm["title"]
        self.form['description'] = requestForm["description"]
        self.form['aid'] = requestForm["aid"]
        self.form['sid'] = requestForm["sid"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form['openDate']):
            inputError['openDate'] = "Open Date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['openDate']):
                inputError['openDate'] = "Incorrect Open Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['title'])):
            self.form["error"] = True
            inputError["title"] = "title can not be null"
        elif (DataValidator.max_len_50(self.form['title'])):
            inputError['title'] = "title can should be below 50 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['title'])):
                inputError['title'] = "title contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            self.form["error"] = True
            inputError["description"] = "description can not be null"
        elif (DataValidator.max_len_100(self.form['description'])):
            inputError['description'] = "description can should be below 100 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['description'])):
                inputError['description'] = "description contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['aid'])):
            self.form["error"] = True
            inputError["aid"] = "Assign To can not be null"


        if (DataValidator.isNull(self.form['sid'])):
            self.form["error"] = True
            inputError["sid"] = "Status can not be null"



        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if DataValidator.isNotNull(self.form['openDate']):
            if DataValidator.isDate(self.form['openDate']):
                inputError['openDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form['title'])):
            if (DataValidator.max_len_50(self.form['title'])):
                inputError['title'] = "title can should be below 50 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['title'])):
                    inputError['title'] = "title contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['description'])):
            if (DataValidator.max_len_100(self.form['description'])):
                inputError['description'] = "description can should be below 100 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['description'])):
                    inputError['description'] = "description contains only letters"
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
            params["openDate"] = json_request.get("openDate", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Issue.objects.last().id
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
            params["openDate"] = json_request.get("openDate", None)
            params["title"] = json_request.get("title", None)
            params["aid"] = json_request.get("aid", None)
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
                res["LastId"] = Issue.objects.last().id
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
        preload_response = self.preload1(None).content.decode()
        preload_data = json.loads(preload_response)
        preload_list = preload_data["preloadList1"]

        r = UserService().get(self.form["aid"])
        index = self.find_dict_index(preload_list, 'sid', self.form['sid'])


        print("ORS API Issue ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.openDate = self.form["openDate"]
        obj.title = self.form["title"]
        obj.description = self.form["description"]
        obj.assignTo = r.login_id
        obj.status = preload_list[index]['status']
        obj.sid = self.form["sid"]
        obj.aid = self.form["aid"]
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
                dup = Issue.objects.exclude(id=self.form['id']).filter(title=self.form["title"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "Title already exists"
                else:
                    r = self.form_to_model(Issue())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Issue.objects.filter(title=self.form["title"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "Title already exists"
                else:
                    r = self.form_to_model(Issue())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Issue
    def get_service(self):
        return IssueService()
