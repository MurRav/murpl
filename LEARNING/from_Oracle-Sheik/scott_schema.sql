SET TERMOUT ON
prompt Building demonstration tables.  Please wait.
SET TERMOUT OFF
SET FEEDBACK OFF

SET LINESIZE 80
SET PAGESIZE 66

ALTER SESSION SET NLS_LANGUAGE = AMERICAN;
ALTER SESSION SET NLS_TERRITORY = AMERICA;

REM Creates tables Emp, Dept, SalGrade, Prod, and Vend.
REM Be sure tables with these names are not critical to your database

-- echo Building CIS 52 demonstration tables.  Please wait.
DROP TABLE Emp CASCADE CONSTRAINTS;
DROP TABLE Dept;
DROP TABLE SalGrade;
DROP TABLE Prod CASCADE CONSTRAINTS;
DROP TABLE Vend;
DROP TABLE PriceCat;

CREATE TABLE DEPT
(   DEPTNO NUMBER(2)     PRIMARY KEY,
    DNAME  VARCHAR2(14),
    LOC    VARCHAR2(13)
);

INSERT INTO DEPT VALUES (10, 'ACCOUNTING', 'NEW YORK');
INSERT INTO DEPT VALUES (20, 'RESEARCH',   'DALLAS');
INSERT INTO DEPT VALUES (30, 'SALES',      'CHICAGO');
INSERT INTO DEPT VALUES (40, 'OPERATIONS', 'BOSTON');

CREATE TABLE Emp
(  EmpNo               NUMBER(4) NOT NULL,
   EName               VARCHAR2(10),
   Job                 CHAR(9),
   Mgr                 NUMBER(4),
   HireDate            DATE,
   Sal                 NUMBER(7,2),
   Comm                NUMBER(7,2),
   DeptNo              NUMBER(2) NOT NULL,
   CONSTRAINT Emp_DeptNo_fk FOREIGN KEY (DeptNo)
              REFERENCES Dept(DeptNo),
   CONSTRAINT Emp_pk PRIMARY KEY (EmpNo)
);

INSERT INTO EMP VALUES
(  7369, 'SMITH',  'CLERK',     7902,
   TO_DATE('17-DEC-1980', 'DD-MON-YYYY'),  800, NULL, 20);
INSERT INTO EMP VALUES
(  7499, 'ALLEN',  'SALESMAN',  7698,
   TO_DATE('20-FEB-1981', 'DD-MON-YYYY'), 1600,  300, 30);
INSERT INTO EMP VALUES
(  7521, 'WARD',   'SALESMAN',  7698,
   TO_DATE('22-FEB-1981', 'DD-MON-YYYY'), 1250,  500, 30);
INSERT INTO EMP VALUES
(  7566, 'JONES',  'MANAGER',   7839,
   TO_DATE('2-APR-1981', 'DD-MON-YYYY'),  2975, NULL, 20);
INSERT INTO EMP VALUES
(  7654, 'MARTIN', 'SALESMAN',  7698,
   TO_DATE('28-SEP-1981', 'DD-MON-YYYY'), 1250, 1400, 30);
INSERT INTO EMP VALUES
(  7698, 'BLAKE',  'MANAGER',   7839,
   TO_DATE('1-MAY-1981', 'DD-MON-YYYY'),  2850, NULL, 30);
INSERT INTO EMP VALUES
(  7782, 'CLARK',  'MANAGER',   7839,
   TO_DATE('9-JUN-1981', 'DD-MON-YYYY'),  2450, NULL, 10);
INSERT INTO EMP VALUES
(  7788, 'SCOTT',  'ANALYST',   7566,
   TO_DATE('09-DEC-1982', 'DD-MON-YYYY'), 3000, NULL, 20);
INSERT INTO EMP VALUES
(  7839, 'KING',   'PRESIDENT', NULL,
   TO_DATE('17-NOV-1981', 'DD-MON-YYYY'), 5000, NULL, 10);
INSERT INTO EMP VALUES
(  7844, 'TURNER', 'SALESMAN',  7698,
   TO_DATE('8-SEP-1981', 'DD-MON-YYYY'),  1500,    0, 30);
INSERT INTO EMP VALUES
(  7876, 'ADAMS',  'CLERK',     7788,
   TO_DATE('12-JAN-1983', 'DD-MON-YYYY'), 1100, NULL, 20);
INSERT INTO EMP VALUES
(  7900, 'JAMES',  'CLERK',     7698,
   TO_DATE('3-DEC-1981', 'DD-MON-YYYY'),   950, NULL, 30);
INSERT INTO EMP VALUES
(  7902, 'FORD',   'ANALYST',   7566,
   TO_DATE('3-DEC-1981', 'DD-MON-YYYY'),  3000, NULL, 20);
INSERT INTO EMP VALUES
(  7934, 'MILLER', 'CLERK',     7782,
   TO_DATE('23-JAN-1982', 'DD-MON-YYYY'), 1300, NULL, 10);

ALTER TABLE Emp ADD
   CONSTRAINT Emp_EmpNo_Mgr_fk FOREIGN KEY (Mgr)
              REFERENCES Emp(EmpNo);

CREATE TABLE SalGrade
(  Grade               NUMBER,
   LoSal               NUMBER,
   HiSal               NUMBER
);

INSERT INTO SalGrade VALUES (1,  700, 1200);
INSERT INTO SalGrade VALUES (2, 1201, 1400);
INSERT INTO SalGrade VALUES (3, 1401, 2000);
INSERT INTO SalGrade VALUES (4, 2001, 3000);
INSERT INTO SalGrade VALUES (5, 3001, 9999);

CREATE TABLE Prod 
(  ProdNo        NUMBER(4)      NOT NULL,
   PName         VARCHAR2(10),
   Type          CHAR(4),
   Family        NUMBER(4),
   Price         NUMBER(7, 2),
   Disc          NUMBER(3, 1),
   IntroDate     DATE,
   VendNo        NUMBER(4),
   Inv           NUMBER(3),
   PRIMARY KEY (ProdNo)
);

INSERT INTO Prod VALUES 
(  4186, 'Lotus 123',  'SPSH', 2215, 349.95,   25, '08-MAY-2001', 26,
   35);
INSERT INTO Prod VALUES 
(  2215, 'Windows',    'OS',   NULL,    129,   40, '15-JAN-2002', 12,
   123);
INSERT INTO Prod VALUES 
(  4003, 'Excel',      'SPSH', 2215, 349.95,   25, '02-AUG-2001', 12,
   22);
INSERT INTO Prod VALUES 
(  1108, 'Finance',    'BUS',  4186,  99.95, NULL, '22-APR-2001', 82,
   16);
INSERT INTO Prod VALUES 
(  8918, 'SQL Server', 'DBMS', 2215,    129,   40, '23-APR-2002', 12,
   123);
INSERT INTO Prod VALUES 
(  6240, 'WordPro',    'WP',   2215,  295.5, 33.3, '01-JUN-1999', 26,
   17);
INSERT INTO Prod VALUES 
(  3055, 'Lotus 123',  'SPSH', 3088, 399.95,    0, '18-OCT-2000', 26,
   12);
INSERT INTO Prod VALUES 
(  3088, 'Macintosh',  'OS',   NULL, 149.95, NULL, '12-APR-2002', 41,
   142);
INSERT INTO Prod VALUES 
(  9518, 'Notes',      'BUS',  2215, 399.95,    0, '27-OCT-2001', 26,
   42);
INSERT INTO Prod VALUES 
(  2910, 'Word',       'WP',   2215,    195,   25, '16-MAY-2000', 12,
   17);
INSERT INTO Prod VALUES 
(  7591, 'Word',       'WP',   3088, 249.95,   25, '16-MAY-2000', 12,
   41);
INSERT INTO Prod VALUES 
(  6482, 'BusPlan',    'BUS',  4186,   54.5,   10, '05-JAN-2001', 82,
   36);
INSERT INTO Prod VALUES 
(  7190, 'BusPlan',    'BUS',  4003,   54.5,   10, '14-FEB-2000', 82,
   NULL);
INSERT INTO Prod VALUES 
(  6888, 'BusPlan',    'BUS',  3055,   54.5,    0, '19-MAY-2001', 82,
   26);
INSERT INTO Prod VALUES 
(  3981, 'SQL*Report', 'DBMS', 5476,  149.5,    0, '22-SEP-2000', 58,
   12);
INSERT INTO Prod VALUES 
(  1067, 'Finance',    'BUS',  3055,  99.95, NULL, '07-MAR-2001', 82,
   0);
INSERT INTO Prod VALUES 
(  5476, 'Oracle',     'DBMS', 2215,    895,    5, '12-SEP-2001', 58,
   38);
INSERT INTO Prod VALUES 
(  8120, 'Inventory',  'BUS',  4003,  199.5,   10, '06-NOV-1999', 82,
   0);
INSERT INTO Prod VALUES 
(  1830, 'SQL*Plus',   'DBMS', 5476,  199.5,    5, '06-OCT-2001', 58,
   19);

CREATE TABLE Vend
(  VName         VARCHAR2(10),
   VState        CHAR(2),
   VendNo        NUMBER(2)   NOT NULL,
   Terms         VARCHAR2(5),
   PRIMARY KEY (VendNo)
);

INSERT INTO Vend VALUES 
(  'Apple',     'CA', 41, 'COD');
INSERT INTO Vend VALUES 
(  'Oracle',    'CA', 58, '30');
INSERT INTO Vend VALUES 
(  'Lotus',     'UT', 26, '30');
INSERT INTO Vend VALUES 
(  'Microsoft', 'WA', 12, '10');
INSERT INTO Vend VALUES 
(  'Acme',      'UT', 82, 'COD');
INSERT INTO Vend VALUES 
(  'Ace',       'OR', 67, '30');

CREATE TABLE PriceCat
(  Category     VARCHAR2(8),
   Low          NUMBER(7, 2),
   High         NUMBER(7, 2)
);

INSERT INTO PriceCat VALUES
(  'Tin',      0,   99.99);
INSERT INTO PriceCat VALUES
(  'Silver',   100, 199.99);
INSERT INTO PriceCat VALUES
(  'Gold',     200, 299.99);
INSERT INTO PriceCat VALUES
(  'Platinum', 300, 10000);

ALTER USER Scott IDENTIFIED by Tiger;

COMMIT;

SET TERMOUT ON
SET FEEDBACK ON


