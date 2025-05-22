from service.models import Task
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Task business logics
'''


class TaskService(BaseService):



    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_task where 1=1"
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("----------", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'creationDate', 'taskTitle', 'details', 'assignTo','taskStatus','aid','sid')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        print("MMMMMMMMMM", params.get("MaxId"))
        return res

    def search1(self, params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        print("-------pageNo-->>", pageNo)
        sql = "select * from sos_task where 1!=1"
        val1 = params.get("creationDate", None)
        val2 = params.get("taskTitle", None)
        val3 = params.get("aid", None)
        val4 = params.get("sid", None)

        print("-----val-->>", val1)
        if DataValidator.isNotNull(val1):
            sql += " or creationDate = '" + str(val1) + "'"
        if DataValidator.isNotNull(val2):
            sql += " or taskTitle like '" + str(val2) + "%%' "
        if DataValidator.isNotNull(val3):
            sql += " or aid = '" + str(val3) + "' "

        if DataValidator.isNotNull(val4):
            sql += " or sid =  '" + str(val4) + "' "


            print("-------sql-->>", sql)
        sql += " limit %s,%s"
        print("-------sql-->>", sql)
        cursor = connection.cursor()
        params["index"] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'creationDate', 'taskTitle', 'details', 'assignTo','taskStatus','aid','sid')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            # print("--------with column-->>",{columnName[i] :  x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            print("-------params['MaxId']-->>", params['MaxId'])
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Task

