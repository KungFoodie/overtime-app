import sqlite3
from Capstone.Python import employee, linkedlist, dbtools as db
import os

# get current directory
path = os.getcwd()

# parent directory
parent = os.path.dirname(path)

# database path
database = parent + '\\database\\employees.sqlite'

template = path

def generate_list():
    emp_list = linkedlist.LinkedList()
    conn = db.connect()
    c = conn.cursor()
    db.create()
    headers = ['key', 'empid', 'fname', 'lname', 'phone', 'job', 'shift', 'call', 'hours']

    temp_data = {}
    total_rows = 0
    data = {}
    for row in c.execute('SELECT * FROM employee_records'):
        i = 0
        for head in headers:
            temp_data[head] = row[i]
            i += 1

        total_rows += 1
        data[total_rows] = temp_data
        temp_data = {}

    for i in range(0, total_rows):
        j = i + 1
        emp = employee.Employee(data[j]['empid'], data[j]['fname'], data[j]['lname'], data[j]['phone'],
                                data[j]['shift'], data[j]['job'], data[j]['hours'], data[j]['call'])
        emp_list.insert_order(emp)

    return emp_list


def generate_list_by_job(job):
    emp_list = linkedlist.LinkedList()

    conn = db.connect()
    c = conn.cursor()
    db.create()
    headers = ['key', 'empid', 'fname', 'lname', 'phone', 'job', 'shift', 'call', 'hours']

    temp_data = {}
    total_rows = 0
    data = {}
    for row in c.execute('SELECT * FROM employee_records WHERE job=?', (job,)):
        i = 0
        for head in headers:
            temp_data[head] = row[i]
            i += 1

        total_rows += 1
        data[total_rows] = temp_data
        temp_data = {}

    for i in range(0, total_rows):
        j = i + 1
        emp = employee.Employee(data[j]['empid'], data[j]['fname'], data[j]['lname'], data[j]['phone'],
                                data[j]['shift'], data[j]['job'], data[j]['hours'], data[j]['call'])
        emp_list.insert_order(emp)

    return emp_list


def generate_table_by_job(emp_list: linkedlist.LinkedList, htmlname):

    html = template + '\\templates\\' + htmlname
    if emp_list.get_node_count() == 0:
        body = "No Employees Found In System"
        with open(html, mode='w') as html:
            html.write(body)
    else:
        page_start = "<div class=\"employeetable\">\n" \
                     "\t<table>\n" \
                     "\t\t<thead>\n" \
                     "\t\t\t<th class=\"colhead\">Employee ID</th>\n" \
                     "\t\t\t<th class=\"colhead\">Name</th>\n" \
                     "\t\t\t<th class=\"colhead\">Hours</th>\n" \
                     "\t\t\t<th class=\"colhead\">Phone</th>\n" \
                     "\t\t\t<th class=\"colhead\">Shift</th>\n" \
                     "\t\t</thead>\n"

        node: employee.Employee = emp_list.head
        body = ""

        j = -1
        for i in range(0, emp_list.get_node_count()):

            if node.get_call() == 'Yes':
                j += 1
                if j % 2 == 0:
                    rowclass = "roweven"
                else:
                    rowclass = "rowodd"

                body += "\t\t<tr class=\""+rowclass+"\">\n" \
                        "\t\t\t<td class=\"coleven\">" + str(node.get_empid()) + "</td>\n" \
                        "\t\t\t<td class=\"colodd\">" + node.get_name() + "</td>\n" \
                        "\t\t\t<td class=\"coleven\">" + str(node.get_hours()) + "</td>\n" \
                        "\t\t\t<td class=\"colodd\">" + node.get_phone() + "</td>\n" \
                        "\t\t\t<td class=\"coleven\">" + node.get_shift() + "</td>\n" \
                        "\t\t</tr>\n"
            node = node.next

        page_end = "\t</table>\n" \
                   "</div>"

        page = page_start + body + page_end
        with open(html, mode='w') as html:
            html.write(page)


def generate_admin_table():
    emp_list = generate_list()

    html = template + '\\templates\\admintable.html'
    if emp_list.get_node_count() == 0:
        body = "No Employees Found In System"
        with open(html, mode='w') as html:
            html.write(body)
    else:
        page_start = "<div class=\"employeetable\">\n" \
                     "\t<table id=\"admintable\">\n" \
                     "\t\t<thead>\n" \
                     "\t\t\t<th class=\"colhead\">Employee ID</th>\n" \
                     "\t\t\t<th class=\"colhead\">Name</th>\n" \
                     "\t\t\t<th class=\"colhead\">Hours</th>\n" \
                     "\t\t\t<th class=\"colhead\">Phone</th>\n" \
                     "\t\t\t<th class=\"colhead\">Shift</th>\n" \
                     "\t\t\t<th class=\"colhead\">Position</th>\n" \
                     "\t\t\t<th class=\"colhead\">Call Status</th>\n" \
                     "\t\t</thead>\n"

        node: employee.Employee = emp_list.head
        body = ""

        for i in range(0, emp_list.get_node_count()):

            if i % 2 == 0:
                rowclass = "roweven"
            else:
                rowclass = "rowodd"

            body += "\t\t<tr class=\""+rowclass+"\">\n" \
                    "\t\t\t<td class=\"coleven\">" + str(node.get_empid()) + "</td>\n" \
                    "\t\t\t<td class=\"colodd\">" + node.get_name() + "</td>\n" \
                    "\t\t\t<td class=\"coleven\">" + str(node.get_hours()) + "</td>\n" \
                    "\t\t\t<td class=\"colodd\">" + node.get_phone() + "</td>\n" \
                    "\t\t\t<td class=\"coleven\">" + node.get_shift() + "</td>\n" \
                    "\t\t\t<td class=\"colodd\">" + node.get_job() + "</td>\n" \
                    "\t\t\t<td class=\"coleven\">" + node.get_call() + "</td>\n" \
                    "\t\t</tr>\n"
            node = node.next

        page_end = "\t</table>\n" \
                   "</div>"

        page = page_start + body + page_end
        with open(html, mode='w') as html:
            html.write(page)


def mod_employee_hours(name, hours):
    conn = sqlite3.connect()
    c = conn.cursor()

    names = name.split(" ")
    fname = names[0]
    lname = names[1]

    db.update_hours(conn, c, fname, lname, hours)
    c.close()
    conn.close()


def add_employee(fname, lname, phone, job, shift, call_check='Yes', hours=0):
    conn = sqlite3.connect()
    c = conn.cursor()

    db.create(c)

    db.insert(conn, c, fname, lname, phone, job, shift, call_check, hours)

    c.close()
    conn.close()
