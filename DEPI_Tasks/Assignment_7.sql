CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    dname VARCHAR(100) NOT NULL
);


CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    pname VARCHAR(100) NOT NULL
);

CREATE TABLE work_hours (
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    hours INT NOT NULL,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status INT NOT NULL
);

-------------------------------------

--1--

select * from employees;

CREATE VIEW vw_employee_details AS
SELECT employees.fname, employees.lname,departments.dname
FROM employees
JOIN departments
ON employees.department_id = departments.department_id;

-----------------------------------------------

--2--

CREATE OR Alter VIEW vw_work_hrs AS
SELECT employees.fname, employees.lname, projects.pname, work_hours.hours
FROM employees JOIN work_hours
ON employees.employee_id = work_hours.employee_id
JOIN projects
ON work_hours.project_id = projects.project_id
WHERE employees.department_id = 5;

-------------------------------------------------------

--3--

CREATE VIEW vw_high_status_suppliers AS
SELECT 
    *
FROM 
    suppliers
WHERE 
    status > 15
WITH CHECK OPTION;

--------------------------------------------------------