from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Course, Subject
from service.forms import SubjectForm
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from ..utility.HtmlUtility import HTMLUtility


class SubjectCtl(BaseCtl):
    def preload(self, request, params):

        self.form["course_ID"] = request.POST.get('course_ID', 0)

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["course_ID"] = obj.course_ID

        self.dynamic_preload = CourseService().preload()

        self.form["preload"]["course"] = HTMLUtility.get_list_from_objects(
            'course_ID',
            self.form["course_ID"],
            self.dynamic_preload
        )

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['subjectName'] = requestForm['subjectName']
        self.form['subjectDescription'] = requestForm['subjectDescription']
        self.form['course_ID'] = requestForm['course_ID']

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['subjectName'] = obj.subjectName
        self.form['subjectDescription'] = obj.subjectDescription
        self.form['course_ID'] = obj.course_ID
        self.form['courseName'] = obj.courseName

    def form_to_model(self, obj):
        c = CourseService().get(self.form['course_ID'])
        pk = int(self.form['id'])
        if (pk>0):
            obj.id = pk
        obj.subjectName = self.form['subjectName']
        obj.subjectDescription = self.form['subjectDescription']
        obj.course_ID = self.form['course_ID']
        obj.courseName = c.courseName
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['subjectName'])):
            inputError['subjectName'] = "Subject Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['subjectName'])):
                inputError['subjectName'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['subjectDescription'])):
            inputError['subjectDescription'] = "Subject Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['course_ID'])):
            inputError['course_ID'] = "Course can not be null"
            self.form['error'] = True
        else:
            obj = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form['courseName'] = obj.courseName
        return self.form['error']

    def display(self, request, params={}):
        if (params['id']>0):
            id = params['id']
            r = self.get_service().get(id)
            self.model_to_form(r)
        res = render(request,self.get_template(),{'form':self.form})
        return res

    def submit(self, request, params={}):
        if (params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(subjectName = self.form['subjectName'])
            if dup.count()>0:
                self.form['error'] = True
                self.form['messege'] = "Subject Name already exists"
                res = render(request,self.get_template(),{'form':self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['messege'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                res = render(request,self.get_template(),{'form':self.form})
        else:
            duplicate = self.get_service().get_model().objects.filter(subjectName = self.form['subjectName'])
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['messege'] = "Subject Name already exists"
                res = render(request,self.get_template(),{'form':self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['messege'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
                res = render(request,self.get_template(),{'form':self.form})
        return res


    # Template html of Subject Page
    def get_template(self):
        return "Subject.html"

    def get_service(self):
        return SubjectService()
