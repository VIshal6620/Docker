from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from ..utility.HtmlUtility import HTMLUtility


class UserCtl(BaseCtl):
    def preload(self, request, params):

        self.form["gender"] = request.POST.get('gender', '')
        self.form["role_Id"] = request.POST.get('role_Id', 0)

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["gender"] = obj.gender
            self.form["role_Id"] = obj.role_Id

        self.static_preload = {"Male": "Male", "Female": "Female"}
        self.dynamic_preload = RoleService().preload()

        self.form["preload"]["gender"] = HTMLUtility.get_list_from_dict(
            'gender',
            self.form["gender"],
            self.static_preload
        )
        self.form["preload"]["role"] = HTMLUtility.get_list_from_objects(
            'role_Id',
            self.form["role_Id"],
            self.dynamic_preload
        )

    # Polulate Form from Http request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"].strip()
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = requestForm["role_Id"]

    # Polulate Form from model
    # GET-DISPLAY method calls this function

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = obj.role_Id
        self.form["role_Name"] = obj.role_Name

    # Convert form into module
    def form_to_model(self, obj):
        c = RoleService().get(self.form['role_Id'])
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id = self.form["role_Id"]
        obj.role_Name = c.name
        return obj

    # Validate form

    def input_validation(self):
        super ().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = " Name can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = " Last Name can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["login_id"].strip())):
            inputError["login_id"] = " login can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['login_id'].strip())):
                inputError['login_id'] = "login ID must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "Confirm Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form['confirmpassword'])):
            if (self.form['password'] != self.form['confirmpassword']):
                inputError['confirmpassword'] = "Password and Confirm Password are not same"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob']= "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be null"
            self.form['error']  = True

        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "MobileNumber can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobilenumber'])):
                inputError['mobilenumber'] = "Mobile No should start with 6,7,8,9"
                self.form['error'] =  True

        if (DataValidator.isNull(self.form['role_Id'])):
            inputError['role_Id'] = "Role can not be null"
            self.form['error'] = True
        # else:
        #     o = RoleService().find_by_unique_key(self.form['role_Id'])
        #     self.form['role_Name'] = o.name
        return self.form['error']

        # Display User Page
    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form': self.form})
        return res

        # Submit User Page
    def submit(self, request, params={}):
        if (params['id'] > 0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(login_id=self.form['login_id'])
            if dup.count() > 0:
                self.form['error'] = True
                self.form['messege'] = "Login Id already exists"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['messege'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            duplicate = self.get_service().get_model().objects.filter(login_id=self.form['login_id'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['messege'] = "Login Id already exists"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['messege'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
                res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "User.html"

    def get_service(self):
        return UserService()
