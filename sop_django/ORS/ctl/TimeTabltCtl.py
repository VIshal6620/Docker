from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import TimeTable
from service.forms import TimeTableForm
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from service.service.TimeTableService import TimeTableService
from ..utility.HtmlUtility import HTMLUtility


class TimeTableCtl(BaseCtl):



    def preload(self, request, params):

        self.form['examTime'] = request.POST.get('examTime','')
        self.form['semester'] = request.POST.get('semester','')
        self.form["course_ID"] = request.POST.get('course_ID', '')
        self.form["subject_ID"] = request.POST.get('subject_ID', 0)

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form['examTime'] = obj.examTime
            self.form['semester'] = obj.semester
            self.form["course_ID"] = obj.course_ID
            self.form["subject_ID"] = obj.subject_ID

        semester_list = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8"}
        examTime_list = {"9:00 AM to 1:00 PM": "9:00 AM to 1:00 PM", "2:00 PM to 4:00 PM": "2:00 PM to 4:00 PM",
                         "4:00 PM to 7:00 PM": "4:00 PM to 7:00 PM"}
        course_list = CourseService().preload()
        subject_list = SubjectService().preload()

        self.form["preload"]["semester"] = HTMLUtility.get_list_from_dict(
            'semester',
            self.form["semester"],
            semester_list
        )
        self.form["preload"]["examTime"] = HTMLUtility.get_list_from_dict(
            'examTime',
            self.form["examTime"],
            examTime_list
        )

        self.form["preload"]["course"] = HTMLUtility.get_list_from_objects(
            'course_ID',
            self.form["course_ID"],
            course_list
        )
        self.form["preload"]["subject"] = HTMLUtility.get_list_from_objects(
            'subject_ID',
            self.form["subject_ID"],
            subject_list
        )

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['examTime'] = requestForm['examTime']
        self.form['examDate'] = requestForm['examDate']
        self.form['subject_ID'] = requestForm['subject_ID']
        self.form['course_ID'] = requestForm['course_ID']
        self.form['semester'] = requestForm['semester']

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['examTime'] = obj.examTime
        self.form['examDate'] = obj.examDate.strftime("%Y-%m-%d")
        self.form['subject_ID'] = obj.subject_ID
        self.form['course_ID'] = obj.course_ID
        self.form['subjectName'] = obj.subjectName
        self.form['courseName'] = obj.courseName
        self.form['semester'] = obj.semester

    def form_to_model(self, obj):
        c = CourseService().get(self.form['course_ID'])
        s = SubjectService().get(self.form['subject_ID'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.examTime = self.form['examTime']
        obj.examDate = self.form['examDate']
        obj.semester = self.form['semester']
        obj.course_ID = self.form['course_ID']
        obj.subject_ID = self.form['subject_ID']
        obj.courseName = c.courseName
        obj.subjectName = s.subjectName
        return obj

    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['examTime'])):
            inputError['examTime'] = "Exam Time can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['examDate'])):
            inputError['examDate'] = "Exam Date can not be null"
            self.form['error'] = True
        if (DataValidator.isNotNull(self.form['examDate'])):
            if (DataValidator.isDate(self.form['examDate'])):
                inputError['examDate'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['course_ID'])):
            inputError['course_ID'] = "Course can not be null"
            self.form['error'] = True
        else:
            o = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form['courseName'] = o.courseName

        if (DataValidator.isNull(self.form['subject_ID'])):
            inputError['subject_ID'] = "Subject can not be null"
            self.form['error'] = True
        else:
            o = SubjectService().find_by_unique_key(self.form['subject_ID'])
            self.form['subjectName'] = o.subjectName

        if (DataValidator.isNull(self.form['semester'])):
            inputError['semester'] = "Semester can not be null"
            self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(),
                     {'form': self.form})
        return res

    def submit(self, request, params={}):
        if (params['id'] > 0):
            q = TimeTable.objects.exclude(id=params["id"]).filter(subject_ID=self.form['subject_ID'],
                                                                  examTime=self.form['examTime'],
                                                                  examDate=self.form['examDate'])
            print("===", q)
            if (q.count() > 0):
                self.form['error'] = True
                self.form['messege'] = "Exam time,Exam date,Subject name already exists"
                return render(request, self.get_template(),
                              {'form': self.form})
            else:
                r = self.form_to_model(TimeTable())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['messege'] = "DATA HAS BEEN UPDATED SUCCESSFULLY"
                return render(request, self.get_template(),
                              {'form': self.form})
        else:
            r = self.form_to_model(TimeTable())
            self.get_service().save(r)
            self.form['id'] = r.id
            self.form['error'] = False
            self.form['messege'] = "DATA HAS BEEN SAVED SUCCESSFULLY"
            return render(request, self.get_template(),
                          {'form': self.form})

    # Template html of TimeTable page
    def get_template(self):
        return "TimeTable.html"

    def get_service(self):
        return TimeTableService()


















