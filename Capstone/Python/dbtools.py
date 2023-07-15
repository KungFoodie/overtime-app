import sqlite3
import csv
import os

# get current directory
path = os.getcwd()

# parent directory
parent = os.path.dirname(path)

# database path
# database = parent + '\\database\\employees.sqlite'
database = path + '\\database\\employees.sqlite'


def connect():
    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error as e:
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


def write_to_csv(query):
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    try:
        with open("report.csv", 'w+', newline='') as file:
            write = csv.writer(file)
            write.writerow([i[0] for i in c.description])
            write.writerows(c)
    except Exception as e:
        print("Error ", e)
        conn.close()
        return False

    conn.close()
