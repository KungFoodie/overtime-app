from html import escape

from flask import Flask, render_template, request, session, redirect, url_for

import employee
from database_code.checker import status
from database_code import dbtools as db
import logic

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "!@#123$%^456"

database = 'C:\\Users\\willi\\Documents\\Regis\\CS493\\Capstone\\employees.sqlite'


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    gw_list = logic.generate_list_by_job("Gateway")
    tc_list = logic.generate_list_by_job("Tech Control")
    logic.generate_table_by_job(gw_list, "gwtable.html")
    logic.generate_table_by_job(tc_list, "tctable.html")
    return render_template("index.html", logged=check_status())


@app.route('/admin', methods=['GET', 'POST'])
@status
def admin():
    if request.method == 'POST':
        oper = escape(request.form['oper'])
        empid = escape(request.form['adminformid'])
        if oper in ['add', 'remove', 'delete']:
            if oper in ['add', 'remove']:
                hours = int(escape(request.form['adminformtime']))
                if oper == 'remove':
                    hours = -hours
                db.update_hours(empid, hours)

            if oper == 'delete':
                db.delete_row(int(empid))

            logic.generate_admin_table()
            return render_template('admin.html', logged=check_status())
        elif oper == 'view':
            return redirect(url_for('record', empid=empid))
        elif oper == 'generate':
            db.write_to_csv("SELECT * FROM employee_records")
            return render_template('admin.html', logged=check_status())

    logic.generate_admin_table()
    return render_template('admin.html', logged=check_status())


@app.route('/record/<empid>', methods=['GET', 'POST'])
@status
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
            return render_template('add.html', logged=check_status(), submitted=False, errors=True,
                                   message="Duplicate ID not allowed")
        else:
            db.insert(empid, fname, lname, phone, job, shift, call_check, hours)
            logic.generate_admin_table()
            return render_template('add.html', logged=check_status(), submitted=True)
    else:
        return render_template('add.html', logged=check_status(), submitted=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        psw = request.form['psw']

        conn = db.connect(database)
        c = conn.cursor()
        sql = f"SELECT username from users where username='{uname}' AND password='{psw}'"
        c.execute(sql)
        if c.fetchone():
            session['logged_in'] = True
            return redirect(request.referrer)
        else:
            # return redirect(request.referrer)
            return render_template('index.html', failed=True)
    else:
        return redirect(request.referrer)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(request.referrer)


def check_status():
    if 'logged_in' in session:
        return True
    return False


if __name__ == '__main__':
    app.run()
