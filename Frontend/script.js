const API_URL = "http://127.0.0.1:8000";

async function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    let response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email: email, password: password})
    });

    let data = await response.json();

    if (data.status === "success") {

    localStorage.setItem(
        "token",
        data.access_token
    );

    localStorage.setItem(
        "user",
        JSON.stringify(data)
    );

    window.location.href = "dashboard.html";
  
    } else {
        document.getElementById("error").innerText = data.message;
    }
}

function loadDashboard() {
    let user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
        window.location.href = "login.html";
        return;
    }

    document.getElementById("welcomeText").innerText = `Welcome, ${user.name} 👋`;
    document.getElementById("roleText").innerText = `Logged in as ${user.role}`;
    document.getElementById("roleCard").innerText = user.role;

    if (user.role === "Employee" || user.role === "Manager") {
        document.getElementById("formSection").style.display = "none";
    }

    if (user.role === "HR") {
        document.getElementById("deleteBtn").style.display = "none";
    }

    loadEmployees(user);
}

function getFormData() {
    return {
        id: Number(document.getElementById("empId").value),
        name: document.getElementById("empName").value,
        email: document.getElementById("empEmail").value,
        department: document.getElementById("empDepartment").value,
        salary: Number(document.getElementById("empSalary").value),
        role: document.getElementById("empRole").value,
        password: document.getElementById("empPassword").value
    };
}

async function addEmployee() {
    let user = JSON.parse(localStorage.getItem("user"));
    let employee = getFormData();

    let url = user.role === "HR"
        ? `${API_URL}/hr/employee`
        : `${API_URL}/admin/employee`;

    let response = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(employee)
    });

    let data = await response.json();
    document.getElementById("msg").innerText = data.message;

    clearForm();
    loadEmployees(user);
}

async function updateEmployee() {
    let user = JSON.parse(localStorage.getItem("user"));
    let employee = getFormData();

    let url = user.role === "HR"
        ? `${API_URL}/hr/employee/${employee.id}`
        : `${API_URL}/admin/employee/${employee.id}`;

    let response = await fetch(url, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(employee)
    });

    let data = await response.json();
    document.getElementById("msg").innerText = data.message;

    clearForm();
    loadEmployees(user);
}

async function deleteEmployee() {
    let id = document.getElementById("empId").value;

    let response = await fetch(`${API_URL}/admin/employee/${id}`, {
        method: "DELETE"
    });

    let data = await response.json();
    document.getElementById("msg").innerText = data.message;

    clearForm();
    loadEmployees(JSON.parse(localStorage.getItem("user")));
}

async function loadEmployees(user) {
    let url = "";

    if (user.role === "Admin") {
        url = `${API_URL}/admin/employees`;
    } else if (user.role === "HR") {
        url = `${API_URL}/hr/employees`;
    } else if (user.role === "Manager") {
        url = `${API_URL}/manager/team/${user.department}`;
    } else {
        url = `${API_URL}/employee/${user.id}`;
    }

    let response = await fetch(url);
    let data = await response.json();

    let employees = Array.isArray(data) ? data : [data];

    document.getElementById("totalCount").innerText = employees.length;

    let table = document.getElementById("employeeTable");
    table.innerHTML = "";

    employees.forEach(emp => {
        table.innerHTML += `
            <tr onclick="fillForm('${emp.id}', '${emp.name}', '${emp.email}', '${emp.department}', '${emp.salary}', '${emp.role}')">
                <td>${emp.id}</td>
                <td>${emp.name}</td>
                <td>${emp.email}</td>
                <td>${emp.department}</td>
                <td>${emp.salary}</td>
                <td>${emp.role}</td>
            </tr>
        `;
    });
}

function fillForm(id, name, email, department, salary, role) {
    document.getElementById("empId").value = id;
    document.getElementById("empName").value = name;
    document.getElementById("empEmail").value = email;
    document.getElementById("empDepartment").value = department;
    document.getElementById("empSalary").value = salary;
    document.getElementById("empRole").value = role;
    document.getElementById("empPassword").value = "";
}

function clearForm() {
    document.getElementById("empId").value = "";
    document.getElementById("empName").value = "";
    document.getElementById("empEmail").value = "";
    document.getElementById("empDepartment").value = "";
    document.getElementById("empSalary").value = "";
    document.getElementById("empPassword").value = "";
}

async function changePassword() {
    let user = JSON.parse(localStorage.getItem("user"));

    let oldPassword = document.getElementById("oldPassword").value;
    let newPassword = document.getElementById("newPassword").value;

    let response = await fetch(`${API_URL}/change-password`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            id: user.id,
            old_password: oldPassword,
            new_password: newPassword
        })
    });

    let data = await response.json();
    document.getElementById("accountMsg").innerText = data.message;
}

async function changeEmail() {
    let user = JSON.parse(localStorage.getItem("user"));

    let newEmail = document.getElementById("newEmail").value;
    let password = document.getElementById("emailPassword").value;

    let response = await fetch(`${API_URL}/change-email`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            id: user.id,
            password: password,
            new_email: newEmail
        })
    });

    let data = await response.json();
    document.getElementById("accountMsg").innerText = data.message;

    if (data.status === "success") {
        user.email = newEmail;
        localStorage.setItem("user", JSON.stringify(user));
    }
}

function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

if (window.location.pathname.includes("dashboard.html")) {
    loadDashboard();
}