#   Name: William Sung
#   Description: CS493 Capstone
#                Employee Class
import functools
from Capstone.Python import dbtools as db


@functools.total_ordering
class Employee:
    def __init__(self, empid, fname="", lname="", phone="", shift="", job="", hours=0, call="Yes"):
        self._empid = empid
        self._name = fname + " " + lname
        self._phone = phone
        self._hours = hours
        self._shift = shift
        self._call = call
        self._job = job
        self.next = None
        self.prev = None

    def __int__(self):
        return self._empid

    def get_job(self):
        return self._job

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

    def __lt__(self, other):
        return self.get_hours() < other.get_hours()

    def __gt__(self, other):
        return self.get_hours() > other.get_hours()

    def __eq__(self, other):
        return self.get_hours() == other.get_hours()

    def on_leave(self):
        return db.check_on_leave(self._empid)
