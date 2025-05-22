from django.db import models


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def get_key(self):
        return str(self.id)

    def get_value(self):
        return self.name

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return data

    class Meta:
        db_table = 'sos_role'


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login_id = models.EmailField()
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
    mobilenumber = models.CharField(max_length=50, default='')
    role_Id = models.IntegerField()
    role_Name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.firstName + '' + self.lastName

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'login_id': self.login_id,
            'password': self.password,
            'confirmpassword': self.confirmpassword,
            'dob': self.dob,
            'address': self.address,
            'gender': self.gender,
            'mobilenumber': self.mobilenumber,
            'role_Id': self.role_Id,
            'role_Name': self.role_Name
        }

        return data

    class Meta:
        db_table = 'sos_user'


class College(models.Model):
    collegeName = models.CharField(max_length=50)
    collegeAddress = models.CharField(max_length=50)
    collegeState = models.CharField(max_length=50)
    collegeCity = models.CharField(max_length=20)
    collegePhoneNumber = models.CharField(max_length=20)

    def get_key(self):
        return str(self.id)

    def get_value(self):
        return self.collegeName

    def to_json(self):
        data = {
            'id': self.id,
            'collegeName': self.collegeName,
            'collegeAddress': self.collegeAddress,
            'collegeState': self.collegeState,
            'collegeCity': self.collegeCity,
            'collegePhoneNumber': self.collegePhoneNumber
        }
        return data

    class Meta:
        db_table = 'sos_college'


class BaseModel(models.Model):
    def to_json(self):
        data = {}
        return data


class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseDescription = models.CharField(max_length=100)
    courseDuration = models.CharField(max_length=100)

    def get_key(self):
        return str(self.id)

    def get_value(self):
        return self.courseName

    def to_json(self):
        data = {
            'id': self.id,
            'courseName': self.courseName,
            'courseDescription': self.courseDescription,
            'courseDuration': self.courseDuration
        }
        return data

    class Meta:
        db_table = 'sos_course'


class Faculty(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def get_key(self):
        return str(self.id)

    def get_value(self):
        return self.name

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'gender': self.gender,
            'dob': self.dob,
            'college_ID': self.college_ID,
            'collegeName': self.courseName,
            'subject_ID': self.subject_ID,
            'subjectName': self.subjectName,
            'course_ID': self.course_ID,
            'courseName': self.courseName,
        }
        return data

    class Meta:
        db_table = 'sos_faculty'


class Marksheet(models.Model):
    rollNumber = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()

    def to_json(self):
        data = {
            'id': self.id,
            'rollNumber': self.rollNumber,
            'name': self.name,
            'physics': self.physics,
            'chemistry': self.chemistry,
            'maths': self.maths
        }
        return data

    class Meta:
        db_table = 'sos_marksheet'


class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'dob': self.dob,
            'mobileNumber': self.mobileNumber,
            'email': self.email,
            'college_ID': self.college_ID,
            'collegeName': self.collegeName
        }
        return data

    class Meta:
        db_table = 'sos_student'


class Subject(models.Model):
    subjectName = models.CharField(max_length=50)
    subjectDescription = models.CharField(max_length=50)

    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def get_key(self):
        return (self.id)

    def get_value(self):
        return self.subjectName

    def to_json(self):
        data = {
            'id': self.id,
            'subjectName': self.subjectName,
            'subjectDescription': self.subjecDescription,
            # 'dob':self.dob,
            'course_ID': self.course_ID,
            # 'courseName': self.courseName
        }
        return data

    class Meta:
        db_table = 'sos_subject'


class Vehicle(models.Model):
    vehicleId = models.IntegerField()
    vehicleName = models.CharField(max_length=50)
    vehicleType = models.CharField(max_length=50)
    purchaseDate = models.DateField(max_length=20)
    buyerName = models.CharField(max_length=50)
    tid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'vehicleId': self.vehicleId,
            'vehicleName': self.vehicleName,
            'vehicleType': self.vehicleType,
            'purchaseDate': self.purchaseDate,
            'buyerName': self.buyerName,
            'tid': self.tid

        }
        return data

    class Meta:
        db_table = 'sos_vehicle'


class ShoppingCart(models.Model):
    name = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    date = models.DateField(max_length=20)
    quantity = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'product': self.product,
            'date': self.date,
            'quantity': self.quantity,
            'pid': self.pid

        }
        return data

    class Meta:
        db_table = 'sos_shoppingcart'


class Order(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.CharField(max_length=50)
    date = models.DateField(max_length=20)
    amount = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'quantity': self.quantity,
            'product': self.product,
            'date': self.date,
            'amount': self.amount,
            'pid': self.pid

        }
        return data

    class Meta:
        db_table = 'sos_order'


class Issue(models.Model):
    openDate = models.DateField(max_length=20)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    assignTo = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    sid = models.IntegerField(default=0)
    aid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'openDate': self.openDate,
            'title': self.title,
            'description': self.description,
            'assignTo': self.assignTo,
            'status': self.status,
            'sid': self.sid,
            'aid': self.aid
        }
        return data

    class Meta:
        db_table = 'sos_issue'


class Task(models.Model):
    creationDate = models.DateField(max_length=20)
    taskTitle = models.CharField(max_length=50)
    details = models.CharField(max_length=200)
    assignTo = models.CharField(max_length=50)
    taskStatus = models.CharField(max_length=50)
    aid = models.IntegerField(default=0)
    sid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'creationDate': self.creationDate,
            'taskTitle': self.taskTitle,
            'details': self.details,
            'assignTo': self.assignTo,
            'taskStatus': self.taskStatus,
            'aid': self.aid,
            'sid': self.sid,
        }
        return data

    class Meta:
        db_table = 'sos_task'


class PortfolioManagement(models.Model):
    portfolioName = models.CharField(max_length=50)
    initialInvestmentAmount = models.BigIntegerField(default=0)
    riskToleranceLevel = models.CharField(max_length=50)
    investmentStrategy = models.CharField(max_length=250)
    rid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'portfolioName': self.portfolioName,
            'initialInvestmentAmount': self.initialInvestmentAmount,
            'riskToleranceLevel': self.riskToleranceLevel,
            'investmentStrategy': self.investmentStrategy,
            'rid': self.rid

        }
        return data

    class Meta:
        db_table = 'sos_portfoliomanagement'


class Staffmember(models.Model):
    fullName = models.CharField(max_length=50)
    joiningDate = models.DateField(max_length=20)
    division = models.CharField(max_length=50)
    previousEmployer = models.CharField(max_length=50)
    did = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'fullName': self.fullName,
            'division': self.division,
            'joiningDate': self.joiningDate,
            'previousEmployer': self.previousEmployer,
            'did': self.did

        }
        return data

    class Meta:
        db_table = 'sos_staffmember'


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobile = models.BigIntegerField(default=0000000000)
    expertise = models.CharField(max_length=50)
    eid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'mobile': self.mobile,
            'expertise': self.expertise,
            'eid': self.eid,
        }
        return data

    class Meta:
        db_table = 'sos_doctor'


class Lead(models.Model):
    date = models.DateField(max_length=20)
    contactName = models.CharField(max_length=50)
    mobile = models.BigIntegerField(default=0)
    status = models.CharField(max_length=50)
    sid = models.IntegerField(default=0)

    def to_json(self):
        data = {
            'id': self.id,
            'date': self.date,
            'contactName': self.contactName,
            'mobile': self.mobile,
            'status': self.status,
            'sid': self.sid

        }
        return data

    class Meta:
        db_table = 'sos_lead'


class TimeTable(models.Model):
    examTime = models.CharField(max_length=40)
    examDate = models.DateField()
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def get_key(self):
        return (self.id)

    def get_value(self):
        return self.examTime

    def to_json(self):
        data = {
            'id': self.id,
            'examTime': self.examTime,
            'examDate': self.examDate,
            'subject_ID': self.subject_ID,
            'subjectName': self.subjectName,
            'course_ID': self.course_ID,
            'courseName': self.courseName,
            'semester': self.semester
        }
        return data

    class Meta:
        db_table = 'sos_timetable'


class Favorite(models.Model):
    product = models.CharField(max_length=50)
    addedDate = models.DateField()

    def to_json(self):
        data = {
            'id': self.id,
            'product': self.product,
            'addedDate': self.addedDate,
        }
        return data

    class Meta:
        db_table = 'sos_favorite'


class Staff(models.Model):
    fullName = models.CharField(max_length=30)
    joiningDate = models.DateField(max_length=15)
    division = models.CharField(max_length=30)
    previousEmployer = models.CharField(max_length=50)

    class Meta:
        db_table = 'sos_Staff'


class Position(models.Model):
    designation = models.CharField(max_length=50)
    openingDate = models.DateField(max_length=15)
    requiredExperience = models.CharField(max_length=30)
    condition = models.CharField(max_length=30)

    class Meta:
        db_table = 'sos_Position'


class Item(models.Model):
    title = models.CharField(max_length=50)
    overview = models.CharField(max_length=25)
    cost = models.CharField(max_length=30)
    purchaseDate = models.DateField(max_length=15)
    category = models.CharField(max_length=30)

    class Meta:
        db_table = 'sos_Item'


class Attribute(models.Model):
    display = models.CharField(max_length=50)
    dataType = models.CharField(max_length=30)
    isActive = models.CharField(max_length=20)
    description = models.CharField(max_length=40)

    def get_key(self):
        return (self.id)

    def get_value(self):
        return self.isActive

    class Meta:
        db_table = 'sos_Attribute'


class Employee(models.Model):
    fullName = models.CharField(max_length=50)
    userName = models.EmailField(max_length=25)
    password = models.CharField(max_length=15)
    birthDate = models.DateField(max_length=20)
    contactNumber = models.CharField(max_length=15)

    def get_key(self):
        return (self.id)

    def get_value(self):
        return self.userName

    class Meta:
        db_table = 'sos_Employee'
