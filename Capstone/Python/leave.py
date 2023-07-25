import functools
import datetime, time

@functools.total_ordering
class Leave:
    def __init__(self, key, empid, fname, lname, start, end):
        self.key = key
        self.empid = empid
        self.fname = fname
        self.lname = lname
        splitdate = start.split("-")
        self.start = datetime.date(int(splitdate[0]), int(splitdate[1]), int(splitdate[2]))
        splitdate = end.split("-")
        self.end = datetime.date(int(splitdate[0]), int(splitdate[1]), int(splitdate[2]))
        diff = self.end - self.start
        self.coverage = [0] * (diff.days + 1)
        self.next = None
        self.prev = None

    def __int__(self):
        return self.key

    def __gt__(self, other):
        return self.start > other.start

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return self.start == other.start

    def get_start_date(self):
        return self.start.strftime("%m/%d/%Y")

    def get_end_date(self):
        return self.end.strftime("%m/%d/%Y")

    def assign_coverage(self, empid, day):
        self.coverage[day] = empid

    def get_coverage(self, day):
        return self.coverage[day]

    def fully_covered(self):
        for i in self.coverage:
            if i == 0:
                return False
        return True

    def get_leave_arr(self):
        return self.coverage

