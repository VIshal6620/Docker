from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session


from .ctl.LoginCtl import LoginCtl
from .ctl.WelcomeCtl import WelcomeCtl
from .ctl.HomeCtl import HomeCtl
from .ctl.UserCtl import UserCtl
from .ctl.UserListCtl import UserListCtl
from .ctl.CollegeCtl import CollegeCtl
from .ctl.CollegeListCtl import CollegeListCtl
from .ctl.CourseCtl import CourseCtl
from .ctl.CourseListCtl import CourseListCtl
from .ctl.MarksheetCtl import MarksheetCtl
from .ctl.MarksheetListCtl import MarksheetListCtl
from .ctl.MarksheetMeritListCtl import MarksheetMeritListCtl
from .ctl.RoleCtl import RoleCtl
from .ctl.RoleList import RoleListCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.StudentListCtl import StudentListCtl
from .ctl.SubjectCtl import SubjectCtl
from .ctl.SubjectListCtl import SubjectListCtl
from .ctl.AddFacultyCtl import AddFacultyCtl
from .ctl.AddFacultyListCtl import AddFacultyListCtl
from .ctl.TimeTabltCtl import TimeTableCtl
from .ctl.TimeTableListCtl import TimeTableListCtl
from .ctl.ChangePasswordCtl import ChangePasswordCtl
from .ctl.RegistrationCtl import RegistrationCtl
from .ctl.ForgetPasswordCtl import ForgetPasswordCtl
from .ctl.MyProfileCtl import MyProfileCtl
from .ctl.FavoriteCtl import FavoriteCtl
from .ctl.FavoriteListCtl import FavoriteListCtl
from .ctl.StaffCtl import StaffCtl
from .ctl.StaffListCtl import StaffListCtl
from .ctl.PositionCtl import PositionCtl
from .ctl.PositionListCtl import PositionListCtl
from .ctl.ItemCtl import ItemCtl
from .ctl.ItemListCtl import ItemListCtl
from .ctl.AttributeCtl import AttributeCtl
from .ctl.AttributeListCtl import AttributeListCtl
from .ctl.EmployeeCtl import EmployeeCtl
from .ctl.EmployeeListctl import EmployeeListCtl

# Create your views here.

@csrf_exempt
def action(request, page, action=""):
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request, {"id": 0})


'''
Calls respective controller with id
'''

@csrf_exempt
def actionId(request, page="", operation="", id=0):
    path = request.META.get('PATH_INFO')
    print("VVVVVVVVVVVVVVVV", path)
    if request.session.get('user') is not None and page != "":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request, {"id": id})
    elif page == "Registration":
        ctlName = "Registration" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif page == "Home":
        ctlName = "Home" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif page == "ForgetPassword":
        ctlName = "ForgetPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif page == "Login":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        print("MMMMMMMMMMM", request.session.get('msg'))
        res = ctlObj.execute(request, {"id": id })

    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = "Your Session has been Expired, Please Login again"
        res = ctlObj.execute(request, {"id": id, 'path': path})
    return res


@csrf_exempt
def auth(request, page="", operation="", id=0):
    if page == "Logout":
        Session.objects.all().delete()
        request.session['user'] = None
        out = "LOGOUT SUCCESSFULL"
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation, 'out': out})


    return res



def index(request):
    res = render(request, 'project.html')
    return res

# To remove Favicon error


def GET(self):
    return HttpResponse("Hello Guys")
