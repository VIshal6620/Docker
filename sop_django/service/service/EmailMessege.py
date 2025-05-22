from sop_django.settings import EMAIL_HOST_USER


class EmailMessege:

    def __init__(self):
        self.frm = EMAIL_HOST_USER
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = ""
        self.text = ""
        self.type = "html"
        self.attachment = []

