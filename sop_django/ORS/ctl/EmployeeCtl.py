from django.shortcuts import render
from ORS.ctl.BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from service.models import Employee
from service.service.EmployeeService import EmployeeService


class EmployeeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['fullName'] = requestForm['fullName']
        self.form['userName'] = requestForm['userName']
        self.form['password'] = requestForm['password']
        self.form['birthDate'] = requestForm['birthDate']
        self.form['contactNumber'] = requestForm['contactNumber']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.fullName = self.form['fullName']
        obj.userName = self.form['userName']
        obj.password = self.form['password']
        obj.birthDate = self.form['birthDate']
        obj.contactNumber = self.form['contactNumber']
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return obj
        self.form['id'] = obj.id
        self.form['fullName'] = obj.fullName
        self.form['userName'] = obj.userName
        self.form['password'] = obj.password
        self.form['birthDate'] = obj.birthDate
        self.form['contactNumber'] = obj.contactNumber

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['fullName'])):
            inputError['fullName'] = "fullName is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['fullName'])):
                inputError['fullName'] = 'fullName is Checked'
                self.form['error'] = True

        if (DataValidator.isNull(self.form['userName'])):
            inputError['userName'] = "userName is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['userName'])):
                inputError['userName'] = "userName is checked "
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            inputError['password'] = "password is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isNull(self.form['password'])):
                inputError['password'] = "password is Check"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['birthDate'])):
            inputError['birthDate'] = "birthDate is Required"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['birthDate'])):
                inputError['birthDate'] = "birthDate is Required"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['contactNumber'])):
            inputError['contactNumber'] = "contactNumber is Required"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['contactNumber'])):
                inputError['contactNumber'] = "contactNumber is Required"
                self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.model_to_form(obj)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(Employee())
        self.get_service().save(r)
        self.form['messege'] = "Data Successfully Saved"
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Employee.html"

    def get_service(self):
        return EmployeeService()
