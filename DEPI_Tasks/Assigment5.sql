
Create table Departments (
Dept_Id int Primary Key,
dept_Name VARCHAR(100) NOT NULL	
);

insert into Departments Values(1, 'Vodafone');
insert into Departments Values(2, 'Dell');
insert into Departments Values(3, 'Etisalat');

select * from  Departments;

Create Table _Employees(
Emp_Id Int Primary KEY , 
Emp_Name VarChar(100) NOT NULL ,
Dept_Id Int References Departments(Dept_Id),
location VarCHAR(50) NOT NULL
);

INSERT INTO _EMPLOYEES VALUES(1,'AHMED ALI', 2, 'cairo');
INSERT INTO _EMPLOYEES VALUES(2,'MOHAMED AHMED',1,'Alexandria');
INSERT INTO _EMPLOYEES VALUES(3,'AYA ALI',2,'Cairo');
INSERT INTO _EMPLOYEES VALUES(4,'AYA', 3 , 'Cairo');


-- commands : -------

Select * from _EMPLOYEES;

Select emp_id , emp_name , dept_id
from _EMPLOYEES
Where location = 'Cairo'

Select Distinct dept_id 
From _EMPLOYEES;

Create Table _students (
ID Int Primary Key , 
First_Name Varchar(100) NOT NULL,
Last_Name VARCHAR(100) DEFAULT 'unknown',
Address VARCHAR(255) DEFAULT 'N/A',
City VARCHAR(100) DEFAULT 'N/A',
Birth_Date DATE 
);

-- Drop table _students;

INSERT INTO _students (ID,First_Name, Last_Name, Address, City, Birth_Date)   
VALUES (1,'Ahmed', 'Ali', 'Downtown', 'Cairo', '1995-01-01');

UPDATE _students   
SET Address = 'Garden City'   
WHERE Last_Name = 'Ahmed';  


BEGIN TRANSACTION;  

DELETE FROM _students   
WHERE City = 'Cairo';  

ROLLBACK; 