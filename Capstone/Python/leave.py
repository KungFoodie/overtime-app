import functools
import datetime, time

@functools.total_ordering
class Leave:
    def __init__(self, key, empid, fname, lname, start, end):
        self.key = key
        self.empid = empid
        self.fname = fname
        self.lname = lname
        self.start = time.strptime(start, "%Y-%m-%d")
        self.end = time.strptime(end, "%Y-%m-%d")
        self.next = None
        self.prev = None

    def __gt__(self, other):
        return self.start > other.start

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return self.start == other.start

    def get_start_date(self):
        return time.strftime('%m/%d/%Y', self.start)

    def get_end_date(self):
        return time.strftime('%m/%d/%Y', self.end)
