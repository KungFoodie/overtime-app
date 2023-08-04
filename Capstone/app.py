#   Name: William Sung
#   Description: CS493 Capstone
#                Flask app code
import sqlite3
from html import escape
from flask import Flask, render_template, request, session, redirect, url_for
from Capstone.Python.checker import status, admin_status
from Capstone.Python import logic, dbtools as db
import os, threading


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "!@#123$%^456"

# Database Backup Interval in Seconds
backup_interval = 30
# Flag for db backup
backup = False


@app.route('/', methods=['GET', 'POST'])
@app.route('/landing', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        uname = request.form['uname']
        psw = request.form['psw']

        try:
            conn = db.connect()
            c = conn.cursor()
            sql = f"SELECT * from users where username='{uname}' AND password='{psw}'"
            c.execute(sql)
            record = c.fetchone()
            if record:
                session['logged_in'] = True
                admin_check = record[5]
                if admin_check == 'yes':
                    session['admin_logged_in'] = True
                conn.close()
                return redirect(url_for('index'))
            else:
                return render_template('landing.html', alert=True, message="Incorrect Username or Password")

        except sqlite3.Error as e:
            db.create_users_table()
            conn.close()
            return render_template('/', failed=True, alert=True,
                                   message="No users found in system. Default admin generated. Please try again.")
    if check_status():
        return redirect(url_for('index'))

    return render_template("landing.html")


@app.route('/index', methods=['GET', 'POST'])
@status
def index():
    gw_list = logic.generate_list_by_job("Gateway")
    tc_list = logic.generate_list_by_job("Tech Control")
    logic.generate_table_by_job(gw_list, "gwtable.html")
    logic.generate_table_by_job(tc_list, "tctable.html")
    logic.generate_leave_table()
    return render_template("index.html", logged=check_status())


@app.route('/admin', methods=['GET', 'POST'])
@admin_status
def admin():
    if request.method == 'POST':
        oper = escape(request.form['oper'])
        if oper in ['add', 'remove', 'delete']:
            empid = escape(request.form['add-hours-id'])
            if oper in ['add', 'remove']:
                hours = int(escape(request.form['hours']))
                if oper == 'remove':
                    hours = -hours
                errors = db.update_hours(empid, hours)
                if not errors:
                    message = "Successfully Updated Hours"
                else:
                    message = "Could not update hours. Error Encountered: " + str(errors)
            if oper == 'delete':
                errors = db.delete_row(int(empid))
                if not errors:
                    message = "Successfully Deleted Employee"
                else:
                    message = "Could not Delete Employee. Error Encountered: " + str(errors)
                errors = db.delete_leave_by_empid(int(empid))
                if not errors:
                    message += ""
                else:
                    message += "Could not Delete Employee Leave Records. Error Encountered: " + str(errors)
            logic.generate_leave_table()
            logic.generate_admin_table()
            return render_template('admin.html', logged=check_status(), alert=True, message=message)
        elif oper == 'view':
            empid = escape(request.form['add-hours-id'])
            return redirect(url_for('record', empid=empid))
        elif oper == 'generate':
            report_name = escape(request.form['var1'])
            if len(report_name) == 0:
                report_name = "default"
            errors = db.write_to_csv("SELECT * FROM employee_records", report_name)
            if not errors:
                return render_template('admin.html', logged=check_status(), alert=True, message="Generated Report: " +
                                                                                                report_name + ".csv")
            else:
                return render_template('admin.html', logged=check_status(), alert=True, message="Error generating "
                                                                                                "report: " + str(errors))
        elif oper == 'leave':
            emplist = logic.generate_list()

            leave_id = escape(request.form['leave-id'])
            node = emplist.search(int(leave_id))
            names = node.get_name().split(" ")
            fname = names[0]
            lname = names[1]
            start = escape(request.form['start-date'])
            end = escape(request.form['end-date'])
            errors = db.add_leave(leave_id, fname, lname, start, end)
            if not errors:
                message = "Successfully Added Leave"
                logic.generate_leave_table()
            else:
                message = "Could not add leave. Error Encountered: " + str(errors)
            return render_template('admin.html', logged=check_status(), alert=True, message=message)

        elif oper == 'leave-delete':
            leave_id = escape(request.form['leave-id-delete'])
            errors = db.delete_leave(leave_id)
            if not errors:
                message = "Successfully Deleted Leave"
            else:
                message = "Could not delete leave. Error Encounter: " + str(errors)
            logic.generate_leave_table()
            return render_template('admin.html', logged=check_status(), alert=True, message=message)

    logic.generate_leave_table()
    logic.generate_admin_table()
    return render_template('admin.html', logged=check_status())


@app.route('/record/<empid>', methods=['GET', 'POST'])
@admin_status
def record(empid):
    if request.method == 'POST':
        formid = escape(request.form['empid'])
        fname = escape(request.form['firstname'])
        lname = escape(request.form['lastname'])
        phone = escape(request.form['phone'])
        shift = escape(request.form['shift'])
        job = escape(request.form['job'])
        call_check = escape(request.form['call'])

        hours = escape(request.form['hours'])
        db.update_record(empid, fname, lname, phone, job, shift, call_check, hours)
        db.update_leave_record(empid, fname, lname)

        return render_template("record.html", logged=check_status(), prefillid=formid, prefillfname=fname,
                               prefilllname=lname, prefillphone=phone, prefilljob=job,
                               prefillshiftvalue=shift, prefillhours=hours,
                               prefillshift=shift,
                               prefillcall=call_check)

    else:
        emplist = logic.generate_list()
        node = emplist.search(int(empid))
        names = node.get_name().split(" ")
        fname = names[0]
        lname = names[1]
        job = node.get_job()
        return render_template("record.html", logged=check_status(), prefillid=node.get_empid(), prefillfname=fname,
                               prefilllname=lname, prefillphone=node.get_phone(), prefilljobvalue=node.get_job(),
                               prefilljob=job,
                               prefillshiftvalue=node.get_shift(), prefillhours=node.get_hours(),
                               prefillshift=node.get_shift(),
                               prefillcall=node.get_call())


@app.route('/add', methods=['GET', 'POST'])
@admin_status
def add():
    if request.method == 'POST':
        empid = escape(request.form['empid'])
        fname = escape(request.form['firstname'])
        lname = escape(request.form['lastname'])
        phone = escape(request.form['phone'])
        shift = escape(request.form['shift'])
        job = escape(request.form['job'])
        call_check = 'Yes'
        hours = 0
        if db.search_by_id(empid):
            return render_template('add.html', logged=check_status(), submitted=False, alert=True, message="Duplicate Employee ID not Allowed")
        else:
            errors = db.insert(empid, fname, lname, phone, job, shift, call_check, hours)
            logic.generate_admin_table()
            if not errors:
                return redirect(url_for('admin'))
            else:
                return render_template('add.html', logged=check_status(), submitted=False, alert=True,
                                       message="Error Adding Employee: " + errors)
    else:
        return render_template('add.html', logged=check_status(), submitted=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        psw = request.form['psw']

        conn = db.connect()
        c = conn.cursor()
        sql = f"SELECT username from users where username='{uname}' AND password='{psw}'"
        try:
            c.execute(sql)
        except sqlite3.Error as e:
            print("Server: No table found, generated default table. Please try to login with default admin")
            db.create_users_table()
            return render_template('index.html', failed=True, alert=True,
                                   message="No users found in system. Default admin generated. Please try again.")
        if c.fetchone():
            session['logged_in'] = True
            conn.close()
            return redirect(request.referrer)
        else:
            conn.close()
            # return redirect(request.referrer)
            return render_template('index.html', failed=True, alert=True, message="Incorrect Username or Password")
    else:
        return redirect(request.referrer)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    if 'admin_logged_in' in session:
        session.pop('admin_logged_in')
    return redirect(url_for('landing'))


def check_status():
    if 'logged_in' in session:
        return True
    return False


def check_admin_status():
    if 'admin_logged_in' in session:
        return True
    return False


def project_path():
    return os.path.dirname(os.path.abspath(__file__))


def db_path():
    return project_path() + '\\database\\employees.sqlite'


if __name__ == '__main__':
    if backup is True:
        daemon = threading.Thread(target=logic.daemon_function_backup, args=(backup_interval,))
        daemon.start()
    app.run()
