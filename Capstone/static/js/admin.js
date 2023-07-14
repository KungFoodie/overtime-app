function check_for_data() {
    let table = document.getElementById("admintable");

    if (table == null) {
        alert("No Data In System");
        return true;
    } else {
        return false;
    }
}

function generate_report() {
    if(check_for_data()) {
        return false;
    }

    let perform_oper = document.getElementById("oper");
    perform_oper.value = "generate";
    let form = document.getElementById("adminform");
    form.submit();
    alert("Report Generated: report.csv");
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
                    alert("Employee would be left with less than 0 hours");
                    return false;
                }
            }
            return table.rows[i].cells[1].innerText;
        }
    }
    alert("Employee ID not found");
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
        let formid = document.getElementById("adminformid");
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
            let formid = document.getElementById("adminformid");
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
        alert("Hours needs to be greater than 0");
        return false;
    } else {
        let question2 = prompt("Enter Employee ID");
        if (question2 === null) {
            return false;
        }
        let id = Number(question2);

        let id_check = check_ids(id, operation, hours);

        if (id_check) {
            let formhours = document.getElementById("adminformtime");
            formhours.value = question1;
            let formid = document.getElementById("adminformid");
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