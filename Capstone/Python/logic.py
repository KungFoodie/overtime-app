#   Name: William Sung
#   Description: CS493 Capstone
#                App Logic
import sqlite3, os, shutil, time
from Capstone.Python import employee, linkedlist, dbtools as db, leave
from Capstone.app import db_path, project_path

# database path
database = db_path()
# backup database path
database_backup = db_path() + ".bak"

# database_backup = db_path() / ".bak"
# template start
template = project_path()


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


def generate_leave_list():
    leave_list: linkedlist.LinkedList = linkedlist.LinkedList()
    conn = db.connect()
    c = conn.cursor()
    db.create_leave_table()
    headers = ['key', 'empid', 'fname', 'lname', 'start', 'end']

    temp_data = {}
    total_rows = 0
    data = {}
    for row in c.execute('SELECT * FROM leave'):
        i = 0
        for head in headers:
            temp_data[head] = row[i]
            i += 1

        total_rows += 1
        data[total_rows] = temp_data
        temp_data = {}

    for i in range(0, total_rows):
        j = i + 1
        leave_record = leave.Leave(data[j]['key'], data[j]['empid'], data[j]['fname'], data[j]['lname'], data[j]['start'],
                                   data[j]['end'])
        leave_list.insert_order(leave_record)

    return leave_list


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
    page_start = "<div class=\"employeetable\">\n" \
                 "\t<table>\n" \
                 "\t\t<thead>\n" \
                 "\t\t\t<th class=\"colhead\">Employee ID</th>\n" \
                 "\t\t\t<th class=\"colhead\">Name</th>\n" \
                 "\t\t\t<th class=\"colhead\">Hours</th>\n" \
                 "\t\t\t<th class=\"colhead\">Phone</th>\n" \
                 "\t\t\t<th class=\"colhead\">Shift</th>\n" \
                 "\t\t</thead>\n"

    if emp_list.get_node_count() == 0:
        body = "\t\t<tr class=\"no-data\">\n" \
               "\t\t\t<td class=\"coleven\" colspan='5'>No Employee Data Found</td>\n" \
               "\t\t</tr>\n"

    else:

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

                body += "\t\t<tr class=\"" + rowclass + "\">\n" \
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

    if emp_list.get_node_count() == 0:
        body = "\t\t<tr class=\"no-data\">\n" \
               "\t\t\t<td class=\"coleven\" colspan='7'>No Employee Data Found</td>\n" \
               "\t\t</tr>\n"

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

            body += "\t\t<tr class=\"" + rowclass + "\">\n" \
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


def generate_leave_table():
    leave_list: linkedlist.LinkedList = generate_leave_list()

    html = template + '\\templates\\leave.html'
    page_start = "<div class=\"employeetable\">\n" \
                 "\t<table id=\"admintable\">\n" \
                 "\t\t<thead>\n" \
                 "\t\t\t<th class=\"colhead\">Leave ID</th>\n" \
                 "\t\t\t<th class=\"colhead\">Employee ID</th>\n" \
                 "\t\t\t<th class=\"colhead\">Name</th>\n" \
                 "\t\t\t<th class=\"colhead\">Start Date</th>\n" \
                 "\t\t\t<th class=\"colhead\">End Date</th>\n" \
                 "\t\t</thead>\n"

    if leave_list.get_node_count() == 0:
        body = "\t\t<tr class=\"no-data\">\n" \
               "\t\t\t<td class=\"coleven\" colspan='5'>No Leave Data Found</td>\n" \
               "\t\t</tr>\n"

    else:

        node: leave.Leave = leave_list.head
        body = ""

        for i in range(0, leave_list.get_node_count()):

            if i % 2 == 0:
                rowclass = "roweven"
            else:
                rowclass = "rowodd"

            body += "\t\t<tr class=\"" + rowclass + "\">\n" \
                    "\t\t\t<td class=\"coleven\">" + str(node.key) + "</td>\n" \
                    "\t\t\t<td class=\"coleven\">" + str(node.empid) + "</td>\n" \
                    "\t\t\t<td class=\"colodd\">" + node.fname + " " + node.lname + "</td>\n" \
                    "\t\t\t<td class=\"coleven\">" + node.get_start_date() + "</td>\n" \
                    "\t\t\t<td class=\"colodd\">" + node.get_end_date() + "</td>\n" \
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


def restore_backup():
    if os.path.exists(database_backup):
        shutil.copy(database_backup, database)
        return True
    else:
        return False


def generate_backup():
    if os.path.exists(database):
        shutil.copy(database, database_backup)
        return True
    else:
        return False


def backup_failover():
    if generate_backup():
        print("Daemon: Backup Generated")
        return True
    elif restore_backup():
        print("Daemon: Backup Restored")
        return True
    else:
        print("Daemon: No database or backup found")
        return False


def daemon_function_backup(interval):
    while True:
        print("Daemon: Starting database fault tolerance checks")
        check = backup_failover()
        if not check:
            db.create_new_db()

        print("Daemon: Finishing database fault tolerance checks")
        time.sleep(interval)
