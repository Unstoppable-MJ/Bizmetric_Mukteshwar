create database HotelManagementSystem


use HotelManagementSystem


create table Menu(
    item varchar(50) primary key,
    price int
)


insert into Menu values
('pizza',120),
('burger',80),
('pasta',100),
('sandwich',70),
('coffee',40),
('tea',20)

create table Bills(
    bill_id int identity(1,1) primary key,
    item varchar(50),
    quantity int,
    amount int,
    bill_date datetime default getdate()
)

