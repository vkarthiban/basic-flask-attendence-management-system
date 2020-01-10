-- CREATE TABLE labourerdata ("labourername" varchar(50),"callbyname" varchar(50),"gender" varchar(50),"dateofbirth" DATE ,"fathername" varchar(50),"bloodgroup" varchar(50),
-- "nextofkin"varchar(40),"contactnumberofnextofkin" varchar(50),"mothertounge"varchar(50),"addressline1"varchar(250),"addressline2"varchar(250),"addressline3"varchar(250),"village"varchar(50),
-- "state"varchar(25),"country"varchar(25),"pincode" varchar(25),"mobilenumber"varchar(250),"residancephonenumber" varchar(250),"emergencyphonenumber"varchar(250));


-- CREATE TABLE  empdata ("dateofjoining" varchar(250),"migrantworker" varchar(250),"siteid" varchar(250),"siteofjoining" varchar(250),"designation" varchar(250),"labourerclass" varchar(250),"wageclass" varchar(250))


-- CREATE TABLE laboureridenty ("documenttype"varchar(40),"documentnumber"varchar(100),"nameasperdoc"varchar(70),delete boolean default False)

-- CREATE TABLE labourerbank ("bankname"varchar(200),"ifsccode"varchar(70),"backaccountnumber"varchar(80),"brancname"varchar(120),"nameinbank"varchar(50));

-- CREATE TABLE attendance("labourerid"varchar(20),"labourername" varchar(30),"labouercategory" varchar(40),"labourertype"varchar(50),"intime" varchar(250),"outtime" varchar(250),"numberofhours"varchar(10),"overtimeallocated" varchar(10),"overtimeworked"varchar(10),"siteid"varchar(50),"projectid" varchar(50),delete boolean default False);


CREATE TABLE  master(username varchar(250),fullname varchar(250),emailid varchar(250),employeeid varchar(250),userrole varchar(250),password bytea,salt bytea,delete boolean default False,archive boolean default False);

-- CREATE TABLE  comaster(username varchar(50),fullname varchar(20),emailid varchar(20),emploeeyid varchar(20),userrole varchar(20),password varchar(40),delete boolean default False,archive boolean default False);

CREATE TABLE applogs(module_name varchar(200), day varchar(200), month varchar(200), year varchar(200), log_severity varchar(300), message varchar(500),userid varchar(200),clientid varchar(20),delete boolean default False);

CREATE TABLE clientusers(username varchar(20),fullname varchar(30),emailid varchar(30),employid varchar(20),designation varchar(30),userrole varchar(30),password varchar(20),delete boolean default False,archive boolean default False);


 create table regusers(clientid text default 'kec'||nextval('regxx'),companyname varchar(250),employeeid varchar(250),username varchar(250),password varchar(250),status varchar(70) default 'unapproved',delete boolean default False,userid varchar(50));

create table syslogg(id serial, progid  VARCHAR(200),timestamp VARCHAR(200),moduleid varchar(50),modekey  varchar(200),event varchar(200),blob VARCHAR(200),finsig   VARCHAR(200),entryid VARCHAR(200))
