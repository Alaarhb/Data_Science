CREATE TABLE employees (
    SSN INT PRIMARY KEY, 
    fname VARCHAR(50), 
    lname VARCHAR(50), 
    hire_date DATE, 
    department_id INT
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY, 
    department_name VARCHAR(100)
);

CREATE TABLE works_on (
    ESSN INT, 
    project_id INT, 
    hours INT,
    PRIMARY KEY (ESSN, project_id),
    FOREIGN KEY (ESSN) REFERENCES employees(SSN)
);

----------------------------------------------
---1---
SELECT *
FROM employees
WHERE hire_date >= DATEADD(day, -30, GETDATE());

---2---
CREATE PROCEDURE sp_get_employee_hours
    @emp_id INT
AS
BEGIN
    SELECT e.fname, e.lname, SUM(w.hours) AS total_hours
    FROM employees e
    JOIN works_on w ON e.SSN = w.ESSN
    WHERE e.SSN = @emp_id
    GROUP BY e.fname, e.lname;
END;

---3---
CREATE PROCEDURE sp_department_employee_count
AS
BEGIN
    SELECT d.department_id, d.department_name, COUNT(e.SSN) AS employee_count
    FROM departments d
    JOIN employees e ON d.department_id = e.department_id
    GROUP BY d.department_id, d.department_name
    HAVING COUNT(e.SSN) > 5;
END;

-------------------------------------------