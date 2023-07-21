function check_for_data() {
    let table = document.getElementById("admintable");
    if (table == null) {
        display_alert("No Data In System");
        return true;
    } else {
        return false;
    }
}

function display_alert(text) {

    document.getElementById("alert").style.display = 'block';

    document.getElementById("alerttext").innerText = text;
}

function generate_report() {
    if(check_for_data()) {
        return false;
    }

    let perform_oper = document.getElementById("oper");
    perform_oper.value = "generate";
    let question1 = prompt("Enter report name");
    let report_name = document.getElementById("var1");
    report_name.value = question1;
    let form = document.getElementById("adminform");
    form.submit();
}

function check_ids(id, operation, hours) {
    if (check_for_data()) {
        return false;
    }
    let table = document.getElementById("admintable");
    let rows = table.rows.length;

    for (let i = 1; i < rows; i++) {
        if (Number(table.rows[i].cells[0].innerText) == id) {
            if (operation === 'remove') {
                if (Number(table.rows[i].cells[2].innerText) - hours < 0) {
                    display_alert("Employee would be left with less than 0 hours");
                    return false;
                }
            }
            return table.rows[i].cells[1].innerText;
        }
    }
    display_alert("Employee ID not found");
    return false;
}

function view_employee() {
    if (check_for_data()) {
        return false;
    }
    let question1 = prompt("Enter ID to view");
    if (question1 === null) {
        return false;
    }
    let empName = check_ids(Number(question1));
    if (empName) {
        let formid = document.getElementById("var1");
        formid.value = question1;
        let perform_oper = document.getElementById("oper");
        perform_oper.value = "view";
        let form = document.getElementById("adminform");
        form.submit();

    } else {
        return false;
    }
}

function delete_employee() {
    if (check_for_data()) {
        return false;
    }
    let question1 = prompt("Enter ID to delete");
    if (question1 === null) {
        return false;
    }
    let empName = check_ids(Number(question1));
    if (empName) {
        if (confirm("Are you sure you want to delete the following Employee?\nEmployee ID: " + question1 +
            "\nName: " + empName)) {
            let formid = document.getElementById("var1");
            formid.value = question1;
            let perform_oper = document.getElementById("oper");
            perform_oper.value = "delete";
            let form = document.getElementById("adminform");
            form.submit();
            window.reload();
        } else {
            return false;
        }

    } else {
        return false;
    }
}

function ask_for_hours(operation) {
    if (check_for_data()) {
        return false;
    }
    let question1 = prompt("Enter number of hours to " + operation);
    if (question1 === null) {
        return false;
    }
    let hours = Number(question1);
    if (hours <= 0) {
        display_alert("Hours needs to be greater than 0");
        return false;
    } else {
        let question2 = prompt("Enter Employee ID");
        if (question2 === null) {
            return false;
        }
        let id = Number(question2);

        let id_check = check_ids(id, operation, hours);

        if (id_check) {
            let formhours = document.getElementById("var2");
            formhours.value = question1;
            let formid = document.getElementById("var1");
            formid.value = question2;
            let perform_oper = document.getElementById("oper");
            perform_oper.value = operation;
            let form = document.getElementById("adminform");
            form.submit();
            return true;
        } else {
            return false;
        }
    }
}


function validate_leave() {

    if(check_for_data()) {
        return false;
    }
    let emp_id = document.getElementById("leave-id").value;

    let failed = false;
    let message = "";

    if (!check_for_id(emp_id)) {
        failed = true;
        message += " Employee ID";
    }

    if (!check_start_date()) {
        failed = true;
        if (message != "") {
            message += ", Start Date";
        } else {
            message += "Start Date";
        }
    }

    if (!check_end_date()) {
        failed = true;
        if (message != "") {
            message += ", End Date";
        } else {
            message += "End Date";
        }
    }

    if (failed) {
        display_alert("Please fix the following fields: " + message);
        return false;
    } else {

        let perform_oper = document.getElementById("oper");
        perform_oper.value = 'leave';

        let form = document.getElementById("leave-form");
        form.submit();
        return true;
    }
}

function check_for_id(empid) {

    let table = document.getElementById("admintable");
    let rows = table.rows.length;
    for (let i = 1; i < rows; i++) {
        if (Number(table.rows[i].cells[0].innerText) == Number(empid)) {

            return true;
        }
    }
    display_alert("Employee ID not found");
    return false;
}


function check_start_date() {
    let start_value = document.getElementById("start-date").value;
    let start_arr = start_value.split("-");
    let start = new Date(start_arr[0] + '/' + start_arr[1] + '/' + start_arr[2]);
    let today = new Date();
    today.setHours(0, 0, 0, 0);
    if (start < today) {
        display_alert("Invalid Start Date");
        return false;
    }
    return true;
}

function check_end_date() {
    let start_value = document.getElementById("start-date").value;
    let start_arr = start_value.split("-");
    let start = new Date(start_arr[0] + '/' + start_arr[1] + '/' + start_arr[2]);
    let end_value = document.getElementById("end-date").value;
    let end_arr = end_value.split("-");
    let end = new Date(end_arr[0] + '/' + end_arr[1] + '/' + end_arr[2]);
    if (end <= start) {
        display_alert("Invalid End Date");
        return false;
    }
    return true;
}

function open_page(page, w, h){
    let width = w;
    let height = h;
    let url = page;

    let leftEdge = window.screenX;
    let topEdge = window.screenY;

    let innerWidth = window.innerWidth;
    let innerHeight = window.innerHeight;

    let topLoc = topEdge + ((innerHeight - height) / 2);
    let leftLoc = leftEdge + ((innerWidth - width) / 2);

    let windowOptions = "menubar=no, width=" + width + ", height=" + height + ", top=" + topLoc + ", left=" + leftLoc;
    window.open(url , 'url', windowOptions);
}