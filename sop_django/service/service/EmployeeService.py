from django.db import connection
from ORS.utility.DataValidator import DataValidator
from service.models import Employee
from service.service.BaseService import BaseService


class EmployeeService(BaseService):

    def search(self, params):
        print('Page No -->', params['pageNo'])
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from sos_Employee where 1=1'
        val = params.get('fullName', None)
        if (DataValidator.isNotNull(val)):
            sql += " and fullName like '" + val + "%%'"
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("------------>", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'fullName', 'userName', "password", "birthDate","contactNumber")
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Employee
