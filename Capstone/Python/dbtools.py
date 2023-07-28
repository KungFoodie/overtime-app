#   Name: William Sung
#   Description: CS493 Capstone
#                Database Tools
import sqlite3
import csv
from datetime import datetime, date

from Capstone.app import db_path, project_path

database = db_path()


def connect():

    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(e)
        return e
    return conn


def close(conn):
    conn.commit()
    conn.close()


def insert(empid, fname, lname, phone, job, shift, call_check, hours):
    conn = connect()
    c = conn.cursor()
    try:
        create()
        with conn:
            c.execute(
                "INSERT INTO employee_records VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (None, empid, fname, lname, phone, job, shift, call_check, hours))
    except sqlite3.Error as e:
        close(conn)
        return e
    close(conn)
    return False


def create():
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS employee_records
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        empid INTEGER,
                        fname TEXT,
                        lname TEXT,
                        phone TEXT,
                        job TEXT,
                        shift TEXT,
                        call_check TEXT,
                        hours INTEGER
                    );
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e
    close(conn)
    return False


def search_by_id(search_id):
    conn = connect()
    c = conn.cursor()
    try:
        create()
        c.execute(f"SELECT * FROM employee_records WHERE empid= ?;",(search_id,))
    except sqlite3.Error as e:
        conn.close()
        return e
    data = c.fetchone()
    close(conn)
    return data


def update_hours(search_id, update):
    conn = connect()
    c = conn.cursor()
    with conn:
        c.execute(f"""UPDATE employee_records
                SET hours = hours + {update}
                WHERE
                    empid = '{search_id}';
                """)
    close(conn)


def update_record(search_id, fname, lname, phone, job, shift, call, hours,):
    conn = connect()
    c = conn.cursor()
    try:
        with conn:
            c.execute(f"""UPDATE employee_records SET 
                    hours= ?,
                    fname= ?,
                    lname= ?,
                    phone= ?,
                    job= ?,
                    shift= ?,
                    call_check=?
                    WHERE
                        empid = '{search_id}';
                    """, (hours, fname, lname, phone, job, shift, call))
    except sqlite3.Error as e:
        close(conn)
        return e

    close(conn)
    return False


def delete_row(deleteid):
    conn = connect()
    c = conn.cursor()
    try:
        with conn:
            c.execute(f"""DELETE FROM employee_records
            WHERE empid={deleteid};
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e

    close(conn)
    return False


def write_to_csv(query, report_name="default"):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute(query)
    except sqlite3.Error as e:
        conn.close()
        return e
    report_path = project_path() + "\\reports\\" + report_name + ".csv"
    try:
        with open(report_path, 'w+', newline='') as file:
            write = csv.writer(file)
            write.writerow([i[0] for i in c.description])
            write.writerows(c)
    except Exception as e:
        print("Error ", e)
        conn.close()
        return e

    conn.close()
    return False


def create_users_table():
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        firstname TEXT,
                        lastname TEXT,
                        password TEXT
                    );
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e
    close(conn)
    add_user("admin", "admin", "account", "admin123")
    return False


def add_user(username, firstname, lastname, password):
    conn = connect()
    c = conn.cursor()
    try:
        create_users_table()
        with conn:
            c.execute(
                "INSERT INTO users VALUES(?, ?, ?, ?, ?)",
                (None, username, firstname, lastname, password))
    except sqlite3.Error as e:
        close(conn)
        return e
    close(conn)
    return False


def create_new_db():
    connect()
    create()
    create_users_table()


def create_leave_table():
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS leave
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        empid INTEGER,
                        firstname TEXT,
                        lastname TEXT,
                        startdate TEXT,
                        enddate TEXT
                    );
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e
    close(conn)
    return False


def add_leave(empid, firstname, lastname, startdate,enddate):
    conn = connect()
    c = conn.cursor()
    try:
        create_leave_table()
        with conn:
            c.execute(
                "INSERT INTO leave VALUES(?, ?, ?, ?, ?, ?)",
                (None, empid, firstname, lastname, startdate, enddate))
    except sqlite3.Error as e:
        close(conn)
        return e
    close(conn)
    return False


def delete_leave(delete_key):
    conn = connect()
    c = conn.cursor()
    try:
        with conn:
            c.execute(f"""DELETE FROM leave
            WHERE id={delete_key};
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e

    close(conn)
    return False


def update_leave(search_id, emp_id, fname, lname, start, end):
    conn = connect()
    c = conn.cursor()
    try:
        with conn:
            c.execute(f"""UPDATE leave SET 
                    empid= ?,
                    firstname= ?,
                    lastname= ?,
                    start= ?,
                    end= ?
                    WHERE
                        id = '{search_id}';
                    """, (emp_id, fname, lname, start, end))
    except sqlite3.Error as e:
        close(conn)
        return e

    close(conn)
    return False


def update_leave_record(emp_id, fname, lname):
    conn = connect()
    c = conn.cursor()
    try:
        with conn:
            c.execute(f"""UPDATE leave SET 
                    firstname= '{fname}',
                    lastname= '{lname}'
                    WHERE
                        empid = '{emp_id}';
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e

    close(conn)
    return False


def delete_leave_by_empid(emp_id):
    conn = connect()
    c = conn.cursor()
    try:
        with conn:
            c.execute(f"""DELETE FROM leave
            WHERE empid={emp_id};
                    """)
    except sqlite3.Error as e:
        close(conn)
        return e

    close(conn)
    return False


def check_on_leave(emp_id):
    conn = connect()
    c = conn.cursor()
    try:
        create_leave_table()
        headers = ['key', 'empid', 'fname', 'lname', 'start', 'end']

        temp_data = {}
        total_rows = 0
        data = {}
        for row in c.execute('SELECT * FROM leave WHERE empid=?', (emp_id,)):
            i = 0
            for head in headers:
                temp_data[head] = row[i]
                i += 1

            total_rows += 1
            data[total_rows] = temp_data
            temp_data = {}

        close(conn)
        for i in range(0, total_rows):
            j = i + 1

            start = data[j]['start']
            end = data[j]['end']

            splitdate = start.split("-")

            start_date = date(int(splitdate[0]), int(splitdate[1]), int(splitdate[2]))
            splitdate = end.split("-")
            end_date = date(int(splitdate[0]), int(splitdate[1]), int(splitdate[2]))
            today = date.today()

            if start_date <= today <= end_date:
                return True

        return False

    except sqlite3.Error as e:
        close(conn)
        return e
