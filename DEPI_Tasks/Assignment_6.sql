CREATE TABLE departments (
    department_id INT PRIMARY KEY,      
    name VARCHAR(100) NOT NULL         
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,         
    name VARCHAR(100) NOT NULL,     
    last_name VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL, 
    manager_id INT,                 
    department_id INT,              
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

INSERT INTO departments (department_id, name)
VALUES 
(1, 'Sales'),
(2, 'Engineering'),
(3, 'HR');

INSERT INTO employees (emp_id, name, last_name, salary, manager_id, department_id)
VALUES 
(101, 'John', 'Doe', 3000, 201, 1),
(102, 'Jane', 'Smith', 4000, 201, 1),
(103, 'Alice', 'Brown', 2500, 200, 2),
(104, 'Bob', 'Johnson', 5000, NULL, 2),
(105, 'Charlie', 'Davis', 3500, 101, 3);


-----------------------Assignment-----------------------------
--1--
SELECT emp_id, last_name, salary
FROM employees
WHERE salary BETWEEN 2000 AND 5000
  AND manager_id NOT IN (101, 200);

--2--
SELECT e.name AS employee_name, d.name AS department_name
FROM employees e
INNER JOIN departments d
  ON e.department_id = d.department_id
ORDER BY d.name ASC;

--3--
SELECT department_id, COUNT(*) AS number_of_employees, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id;
