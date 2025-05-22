from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import PortfolioManagement
from service.service.PortfolioManagementService import PortfolioManagementService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class PortfolioManagementCtl(BaseCtl):

    def preload(self, request, params={}):
        preloadList = [
            {'rid': 1, 'riskToleranceLevel': "Low"},
            {'rid': 2, 'riskToleranceLevel': "Medium"},
            {'rid': 3, 'riskToleranceLevel': "High"},
            
        ]
        return JsonResponse({"preloadList": preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['portfolioName'] = requestForm['portfolioName']
        self.form['initialInvestmentAmount'] = requestForm["initialInvestmentAmount"]
        self.form['rid'] = requestForm["rid"]
        self.form['investmentStrategy'] = requestForm["investmentStrategy"]

    def input_validation(self):
        inputError = self.form["inputError"]



        if (DataValidator.isNull(self.form['portfolioName'])):
            self.form["error"] = True
            inputError["portfolioName"] = "Name can not be null"
        elif (DataValidator.len_btw_3_to_30(self.form['portfolioName'])):
            inputError['portfolioName'] = "Name should be between 3 to 30 characters"
            self.form['error'] = True
        else:
            if (DataValidator.isalphanumeric(self.form['portfolioName'])):
                inputError['portfolioName'] = "Name contains letters and numbers only"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["initialInvestmentAmount"])):
            self.form["error"] = True
            inputError["initialInvestmentAmount"] = "Initial Investment Amount can not be null"
        elif (DataValidator.max_len_20(self.form['initialInvestmentAmount'])):
            inputError['initialInvestmentAmount'] = "initialInvestmentAmount can should be below 20 digit"
            self.form['error'] = True
        elif (DataValidator.isnumb(self.form['initialInvestmentAmount'])):
            inputError['initialInvestmentAmount'] = "Incorrect Initial Investment Amount,Amount should be in numbers"
            self.form['error'] = True
        else:
            if (DataValidator.is_0(self.form['initialInvestmentAmount'])):
                inputError['PortfolioManainitialInvestmentAmountgementId'] = "initialInvestmentAmount can not be 0 or less than 0"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['rid'])):
            self.form["error"] = True
            inputError["rid"] = "Risk Tolerance Level can not be null"



        if (DataValidator.isNull(self.form['investmentStrategy'])):
            self.form["error"] = True
            inputError["investmentStrategy"] = "Investment Strategy can not be null"
        elif (DataValidator.len_btw_10_to_200(self.form['investmentStrategy'])):
            inputError['investmentStrategy'] = "Investment Strategy should be between 10 to 200 characters"
            self.form['error'] = True
        else:
            if (DataValidator.isalphanumeric(self.form['investmentStrategy'])):
                inputError['investmentStrategy'] = "Investment Strategy contains letters and numbers only"
                self.form['error'] = True

        return self.form["error"]

    def input_validation1(self):
        inputError = self.form["inputError"]

        if (DataValidator.isNotNull(self.form['portfolioName'])):
            if (DataValidator.len_btw_3_to_30(self.form['portfolioName'])):
                inputError['portfolioName'] = "Name should be between 3 to 30 characters"
                self.form['error'] = True
            else:
                if (DataValidator.isalphanumeric(self.form['portfolioName'])):
                    inputError['portfolioName'] = "Name contains letters and numbers only"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['rid'])):
            pass

        if DataValidator.isNotNull(self.form['initialInvestmentAmount']):
            if (DataValidator.max_len_20(self.form['initialInvestmentAmount'])):
                inputError['initialInvestmentAmount'] = "initialInvestmentAmount can should be below 20 digit"
                self.form['error'] = True
            elif (DataValidator.isnumb(self.form['initialInvestmentAmount'])):
                inputError[
                    'initialInvestmentAmount'] = "Incorrect Initial Investment Amount,Amount should be in numbers"
                self.form['error'] = True
            else:
                if (DataValidator.is_0(self.form['initialInvestmentAmount'])):
                    inputError[
                        'PortfolioManainitialInvestmentAmountgementId'] = "initialInvestmentAmount can not be 0 or less than 0"
                    self.form['error'] = True

        if (DataValidator.isNotNull(self.form['investmentStrategy'])):
            if (DataValidator.len_btw_10_to_200(self.form['investmentStrategy'])):
                inputError['investmentStrategy'] = "Investment Strategy should be between 10 to 200 characters"
                self.form['error'] = True
            else:
                if (DataValidator.isalphanumeric(self.form['investmentStrategy'])):
                    inputError['investmentStrategy'] = "Investment Strategy contains letters and numbers only"
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
            params["portfolioName"] = json_request.get("portfolioName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        c = self.get_service().search(params)
        res = {"mesg": ""}
        if (c != None):
            res["data"] = c["data"]
            if res["data"] == []:
                res["mesg"] = "No record found"
            res["MaxId"] = c["MaxId"]
            res["index"] = c["index"]
            res["LastId"] = PortfolioManagement.objects.last().id
            res["error"] = False
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"result": res})

    def search1(self, request, params={}):
        res = {}
        json_request = json.loads(request.body)
        json_request['id'] = 0
        json_request['rid'] = 0
        print("----------------------", json_request)

        if (json_request):
            params["portfolioName"] = json_request.get("portfolioName", None)
            params["initialInvestmentAmount"] = json_request.get("initialInvestmentAmount", None)
            params["rid"] = json_request.get("rid", None)
            params["investmentStrategy"] = json_request.get("investmentStrategy", None)
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
                res["LastId"] = PortfolioManagement.objects.last().id
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

        index = self.find_dict_index(preload_list, 'rid', self.form['rid'])

        print("ORS API PortfolioManagement ============ Form to model------------------------")
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.portfolioName = self.form["portfolioName"]
        obj.initialInvestmentAmount = self.form["initialInvestmentAmount"]
        obj.riskToleranceLevel = preload_list[index]["riskToleranceLevel"]
        obj.investmentStrategy = self.form["investmentStrategy"]
        obj.rid = self.form["rid"]
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
                dup = PortfolioManagement.objects.exclude(id=self.form['id']).filter(portfolioName=self.form["portfolioName"])
                if (dup.count() > 0):
                    res["error"] = True
                    res["message"] = "PortfolioManagement Name already exists"
                else:
                    r = self.form_to_model(PortfolioManagement())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Updated Successfully"
                return JsonResponse({"data": res, "form": self.form})
            else:
                duplicate = PortfolioManagement.objects.filter(portfolioName=self.form["portfolioName"])
                if (duplicate.count() > 0):
                    res["error"] = True
                    res["message"] = "PortfolioManagement Name already exists"
                else:
                    r = self.form_to_model(PortfolioManagement())
                    self.get_service().save(r)
                    if (r != None):
                        res["data"] = r.to_json()
                        res["error"] = False
                        res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data": res, "form": self.form})

    # Service of PortfolioManagement
    def get_service(self):
        return PortfolioManagementService()
