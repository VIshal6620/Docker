from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.service.ForgetPasswordService import ForgetPasswordService
from service.service.EmailService import EmailService
from service.service.EmailMessege import EmailMessege
from service.models import User


class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form['login_id'] = requestFrom['login_id']

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['login_id']):
            inputError['login_id'] = "Login Id can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['login_id'])):
                inputError['login_id'] = "login ID must be like student@gmail.com"
                self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        q = User.objects.filter(login_id=self.form['login_id'])
        userList = ""
        for userData in q:
            userList = userData
        if userList != "":
            emsg = EmailMessege()
            emsg.to = [userList.login_id]
            emsg.subject = "Forget Password"
            mailResponse = EmailService.send(emsg, "forgotPassword", userList)
            print("mail:",mailResponse)
            if mailResponse == 1:
                self.form['error'] = False
                self.form['messege'] = "PLEASE CHECK YOUR MAIL, YOUR PASSWORD HAS BEEN SENT SUCCESSFULLY"
                request.session['user'] = userList
                res = render(request, self.get_template(), {'form': self.form})
            else:
                self.form['error'] = True
                self.form['messege'] = "Please check your Internet Connection"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            self.form["error"] = True
            self.form["messege"] = "Login Id is Incorrect"
            res = render(request, self.get_template(), {'form': self.form})
        return res

    # Template Html of Forgetpassword Page
    def get_template(self):
        return "ForgetPassword.html"

    def get_service(self):
        return ForgetPasswordService()
