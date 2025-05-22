from django.shortcuts import render, redirect
from ORS.ctl.BaseCtl import BaseCtl
from service.service.PositionService import PositionService


class PositionListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['designation'] = requestForm.get('designation', None)
        self.form['openingDate'] = requestForm.get('openingDate', None)
        self.form['requiredExperience'] = requestForm.get('requiredExperience', None)
        self.form['condition'] = requestForm.get('condition', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        PositionListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        PositionListCtl.count += 1
        self.form['pageNo'] = PositionListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        PositionListCtl.count -= 1
        self.form['pageNo'] = PositionListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/Position/")
        return res

    def submit(self, request, params={}):
        PositionListCtl.count = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def deleteRecord(self, request, params={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['mesg'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                record = self.get_service().get(id)
                if record:
                    self.get_service().delete(id)
                    self.form['mesg'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['mesg'] = "Data is not deleted"
            self.form['pageNo'] = 1
            records = self.get_service().search(self.form)
            self.page_list = records['data']
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def get_service(self):
        return PositionService()

    def get_template(self):
        return "PositionList.html"
