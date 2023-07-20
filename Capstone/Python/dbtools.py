#   Name: William Sung
#   Description: CS493 Capstone
#                Database Tools
import sqlite3
import csv
from Capstone.app import db_path, project_path

database = db_path()


def connect():

    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error as e:
        print(database)
        print(e)
        return e
    return conn


def close(conn):
    conn.commit()
    conn.close()


def insert(empid, fname, lname, phone, job, shift, call_check, hours):
    conn = connect()
    c = conn.cursor()
    create()
    with conn:
        c.execute(
            "INSERT INTO employee_records VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (None, empid, fname, lname, phone, job, shift, call_check, hours))
    close(conn)


def create():
    conn = connect()
    c = conn.cursor()
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
    close(conn)


def search_by_id(search_id):
    conn = connect()
    c = conn.cursor()
    create()
    c.execute(f"SELECT * FROM employee_records WHERE empid= ?;",(search_id,))
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
    close(conn)


def delete_row(deleteid):
    conn = connect()
    c = conn.cursor()
    with conn:
        c.execute(f"""DELETE FROM employee_records
        WHERE empid={deleteid};
                """)
    close(conn)


def write_to_csv(query, report_name):
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
    c.execute("""CREATE TABLE IF NOT EXISTS users
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    firstname TEXT,
                    lastname TEXT,
                    password TEXT
                );
                """)
    close(conn)
    add_user("admin", "admin", "account", "admin123")


def add_user(username, firstname, lastname, password):
    conn = connect()
    c = conn.cursor()
    create()
    with conn:
        c.execute(
            "INSERT INTO users VALUES(?, ?, ?, ?, ?)",
            (None, username, firstname, lastname, password))
    close(conn)


def create_new_db():
    connect()
    create()
    create_users_table()
