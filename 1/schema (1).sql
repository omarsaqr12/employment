
create table company(
c_name varchar(30),
c_busi_email varchar(50),
c_phone_number int,
c_password varchar(40) not NULL,
c_sector varchar(30),
youtube varchar(50),
linkedin varchar(50),
instagram varchar(50),
facebook varchar(50),
c_found_date date,
PRIMARY key(c_name,c_busi_email,c_phone_number)
);
CREATE TABLE c_location(
c_name VARCHAR(30),
city varchar(20),
country varchar(20),
primary key(c_name,city),
FOREIGN KEY (c_name) REFERENCES company(c_name)
);
CREATE TABLE job(
c_name VARCHAR(30),
c_busi_email varchar(50),
c_phone_number int,
job_requirements VARCHAR(300),
career_level VARCHAR(10),
max_exp int,
min_exp int,
min_salary int,
max_salary int,
title VARCHAR(20) not NULL,
job_description VARCHAR(300),
keywords VARCHAR(100),
educational_level VARCHAR(20),
j_city varchar(20) not NULL,
j_country varchar(20) not NULL,
PRIMARY key(c_name,c_busi_email,c_phone_number,job_requirements),
FOREIGN KEY (c_name,c_busi_email,c_phone_number) REFERENCES company(c_name,c_busi_email,c_phone_number)
);
CREATE TABLE job_category(
c_name VARCHAR(30),
c_busi_email varchar(50),
c_phone_number int,
job_requirements VARCHAR(300) REFERENCES job(job_requirements),
category VARCHAR(30),
PRIMARY key(c_name,c_busi_email,c_phone_number,category,job_requirements),
FOREIGN KEY (c_name,c_busi_email,c_phone_number) REFERENCES company(c_name,c_busi_email,c_phone_number)
);
CREATE TABLE job_type(
c_name VARCHAR(30),
c_busi_email varchar(50),
c_phone_number int,
job_requirements VARCHAR(300) REFERENCES job(job_requirements),
j_type VARCHAR(30),
PRIMARY key(c_name,c_busi_email,c_phone_number,j_type,job_requirements),
FOREIGN KEY (c_name,c_busi_email,c_phone_number) REFERENCES company(c_name,c_busi_email,c_phone_number)
);
CREATE TABLE usere(
u_email VARCHAR(50) primary key,
cv VARCHAR(8000),
u_no_exp int not NULL,
min_salary int,
last_name VARCHAR(10),
m_name VARCHAR(10),
f_name VARCHAR(10)
);
CREATE TABLE personal_information(
u_email VARCHAR(50),
gender char(1) CHECK (gender in ('m','f')),
p_city VARCHAR(20),
p_country VARCHAR(20),
p_area VARCHAR(20),
yera int,
month int,
nationality VARCHAR(15),
phone_number int,
PRIMARY key(u_email,gender),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE experience(start_year int,
start_month int,
end_year int,
end_month int,
job_title VARCHAR(20),
company VARCHAR(30),
u_email VARCHAR(50),
experience_type VARCHAR(30),
PRIMARY key(u_email,experience_type),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE education(
u_email VARCHAR(50),
edate date,
degree_type VARCHAR(20),
field_of_study VARCHAR(25),
university VARCHAR(20),
grade float,
PRIMARY key(u_email,edate),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE user_to_company(
u_email VARCHAR(50) REFERENCES usere(u_email),
c_name VARCHAR(30),
c_busi_email varchar(50),
c_phone_number int,
questions VARCHAR(600),
application_date date,
job_in_ref VARCHAR(300) REFERENCES job(job_requirements),
coverletter varchar(800),
PRIMARY KEY(u_email,c_busi_email,c_name,c_phone_number,job_in_ref),
FOREIGN KEY (c_name,c_busi_email,c_phone_number) REFERENCES company(c_name,c_busi_email,c_phone_number)
);
CREATE TABLE user_skills(
u_email VARCHAR(50),
skills VARCHAR(500),
PRIMARY KEY(u_email,skills),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE user_technology(
u_email VARCHAR(50),
technology VARCHAR(500),
PRIMARY KEY(u_email,technology),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE user_job_cat(
u_email VARCHAR(50),
can_job_category VARCHAR(50),
PRIMARY KEY(u_email,can_job_category),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE user_job_type(
u_email VARCHAR(50),
can_job_type VARCHAR(50),
PRIMARY KEY(u_email,can_job_type),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);
CREATE TABLE user_job_title(
u_email VARCHAR(50),
can_job_title VARCHAR(20),
PRIMARY KEY(u_email,can_job_title),
FOREIGN KEY (u_email) REFERENCES usere(u_email)
);