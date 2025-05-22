from django.shortcuts import render, redirect
from ORS.ctl.BaseCtl import BaseCtl
from service.models import Item
from service.service.AttributeService import AttributeService


class AttributeListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['display'] = requestForm.get('display', None)
        self.form['dataType'] = requestForm.get('dataType', None)
        self.form['isActive'] = requestForm.get('isActive', None)
        self.form['description'] = requestForm.get('description', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        AttributeListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        AttributeListCtl.count += 1
        self.form['pageNo'] = AttributeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        AttributeListCtl.count -= 1
        self.form['pageNo'] = AttributeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/Attribute/")
        return res

    def submit(self, request, params={}):
        AttributeListCtl.count = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = AttributeListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if id > 0:
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                       # self.form['LastId'] = Item.objects.last().id
                        AttributeListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETD"
                        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def get_service(self):
        return AttributeService()

    def get_template(self):
        return "AttributeList.html"
