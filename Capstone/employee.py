class Employee:
    def __init__(self, empid, fname="", lname="", phone="", shift="", job="", hours=0, call="Yes"):
        self._empid = empid
        self._name = fname + " " + lname
        self._phone = phone
        self._hours = hours
        self._shift = shift
        self._call = call
        self.job = job
        self.next = None
        self.prev = None

    def __str__(self):
        return self._name + ' ' + str(self._hours)

    def get_job(self):
        return self.job

    def get_empid(self):
        return self._empid

    def set_hours(self, hours):
        self._hours = hours

    def get_hours(self):
        return self._hours

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_phone(self, phone):
        self._phone = phone

    def get_phone(self):
        return self._phone

    def set_shift(self, shift):
        self._shift = shift

    def get_shift(self):
        return self._shift

    def set_call(self, call):
        self._call = call

    def get_call(self):
        return self._call
