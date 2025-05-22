from django.shortcuts import render
from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from ORS.utility.HtmlUtility import HTMLUtility
from service.models import Position, Attribute
from service.service.AttributeService import AttributeService



class AttributeCtl(BaseCtl):

    def preload(self, request,params):
        self.form['isActive']=request.POST.get('isActive','')

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form['isActive']=obj.isActive


        self.static_preload = {"Yes":"Yes","No":"No"}

        self.form["preload"]["isActive"] = HTMLUtility.get_list_from_dict('isActive',
        self.form['isActive'],
        self.static_preload
                                                                           )

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['display'] = requestForm['display']
        self.form['dataType'] = requestForm['dataType']
        self.form['isActive'] = requestForm['isActive']
        self.form['description'] = requestForm['description']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.display = self.form['display']
        obj.dataType = self.form['dataType']
        obj.isActive = self.form['isActive']
        obj.description = self.form['description']
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return obj
        self.form['id'] = obj.id
        self.form['display'] = obj.display
        self.form['dataType'] = obj.dataType
        self.form['isActive'] = obj.isActive
        self.form['description'] = obj.description

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['display'])):
            inputError['display'] = "display is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['display'])):
                inputError['display'] = 'display is Checked'
                self.form['error'] = True

        if (DataValidator.isNull(self.form['dataType'])):
            inputError['dataType'] = "dataType is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['dataType'])):
                inputError['dataType'] = "dataType is checked "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['isActive'])):
            inputError['isActive'] = "isActive is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isNull(self.form['isActive'])):
                inputError['isActive'] = "isActive is Check"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "description is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['description'])):
                inputError['description'] = "description is Required"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Attribute())
        self.get_service().save(r)
        self.form['messege'] = "Data Successfully Saved"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Attribute.html"

    def get_service(self):
        return AttributeService()
