from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Task
from service.service.TaskService import TaskService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class TaskCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'aid': 1, 'assignTo': 'Raj Singh'},
            {'aid': 2, 'assignTo': 'Jalaj Singh'},
            {'aid': 3, 'assignTo': 'Aman Soni'},
            {'aid': 4, 'assignTo': 'Ajay Sharma'},
            {'aid': 5, 'assignTo': 'Tarun Indoria'},
            {'aid': 6, 'assignTo': 'Rahul Suroliya'},
        ]
        return JsonResponse({"preloadList": preloadList})

    def preload1(self, request, params={}):
        preloadList =[
            {'sid': 1, 'taskStatus':'Open'},
            {'sid': 2, 'taskStatus':'In Progress'},
            {'sid': 3, 'taskStatus':'Hold'},
            {'sid': 4, 'taskStatus':'Resolve'},
            {'sid': 5, 'taskStatus':'Close'}

        ]
        return JsonResponse({"preloadList1": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['creationDate'] = requestForm["creationDate"]
        self.form['taskTitle'] = requestForm["taskTitle"]
        self.form['details'] = requestForm["details"]
        self.form['aid'] = requestForm["aid"]
        self.form['sid'] = requestForm["sid"]

    def input_validation(self):
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form['creationDate']):
            inputError['creationDate'] = "Open Date can not be Null"
            self.form['error'] = True
        else:
            if DataValidator.isDate(self.form['creationDate']):
                inputError['creationDate'] = "Incorrect Open Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['taskTitle'])):
            self.form["error"] = True
            inputError["taskTitle"] = "taskTitle can not be null"
        elif (DataValidator.max_len_20(self.form['taskTitle'])):
            inputError['taskTitle'] = "taskTitle can should be below 20 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['taskTitle'])):
                inputError['taskTitle'] = "taskTitle contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['details'])):
            self.form["error"] = True
            inputError["details"] = "details can not be null"
        elif (DataValidator.max_len_100(self.form['details'])):
            inputError['details'] = "details can should be below 100 character"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['details'])):
                inputError['details'] = "details contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['aid'])):
            self.form["error"] = True
            inputError["aid"] = "Assign To can not be null"


        if (DataValidator.isNull(self.form['sid'])):
            self.form["error"] = True
            inputError["sid"] = "taskStatus can not be null"



        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if DataValidator.isNotNull(self.form['creationDate']):
            if DataValidator.isDate(self.form['creationDate']):
                inputError['creationDate'] = "Incorrect Date format, should be DD-MM-YYYY format and dob should in past or present"
                self.form['error'] = True

        if (DataValidator.isNotNull(self.form['taskTitle'])):
            if (DataValidator.max_len_20(self.form['taskTitle'])):
                inputError['taskTitle'] = "taskTitle can should be below 20 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['taskTitle'])):
                    inputError['taskTitle'] = "taskTitle contains only letters"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['details'])):
            if (DataValidator.max_len_100(self.form['details'])):
                inputError['details'] = "details can should be below 100 character"
                self.form['error'] = True
            else:
                if (DataValidator.isalphacheck(self.form['details'])):
                    inputError['details'] = "details contains only letters"
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
            params["creationDate"] = json_request.get("creationDate", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = Task.objects.last().id
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
            params["creationDate"] = json_request.get("creationDate", None)
            params["taskTitle"] = json_request.get("taskTitle", None)
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
                res["LastId"] = Task.objects.last().id
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

        preload_response = self.preload1(None).content.decode()
        preload_data = json.loads(preload_response)
        preload_list1 = preload_data["preloadList1"]

        index = self.find_dict_index(preload_list, 'aid', self.form['aid'])
        index1 = self.find_dict_index(preload_list1, 'sid', self.form['sid'])


        print("ORS API Task ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.creationDate = self.form["creationDate"]
        obj.taskTitle = self.form["taskTitle"]
        obj.details = self.form["details"]
        obj.assignTo = preload_list[index]['assignTo']
        obj.taskStatus = preload_list1[index1]['taskStatus']
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
                dup = Task.objects.exclude(id=self.form['id']).filter(taskTitle=self.form["taskTitle"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "taskTitle already exists"
                else:
                    r = self.form_to_model(Task())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = Task.objects.filter(taskTitle=self.form["taskTitle"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "taskTitle already exists"
                else:
                    r = self.form_to_model(Task())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of Task
    def get_service(self):
        return TaskService()
