DROP TABLE teacher_info IF EXISTS teacher_info;
CREATE TABLE teacher_info (
    teacher_id int primary key,
    name varchar(50),
    department varchar(100),
    title varchar(50),
    phone varchar(100),
    email varchar(100),
    building varchar(255),
    room varchar(100),
    field text);

