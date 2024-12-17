use sofi;
create table teacher(
name varchar(100),
age int,
salary int,
department varchar(50)
);
create table student(
name varchar(20),
department varchar(50),
marks int
);
alter table teacher add column  degree varchar(100);
alter table student add column city varchar(80);
alter table student change marks marks_scored int;
drop table teacher;
select * from student;
insert into student values("rasni","ece",100,"chennai");
select * from student;
insert into student values("mervin","cse",100,"bangalore");
insert into student values("tharshini","ece",200,"dharmapuri");
update student set department="ECE"



