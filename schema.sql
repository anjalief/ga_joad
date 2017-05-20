drop table if exists members;
create table members (
  id integer primary key autoincrement,
  firstname text not null,
  lastname text not null,
  gender text not null,
  byear date not null
);

drop table if exists member_details;
create table member_details (
  id integer,
  date date not null DEFAULT CURRENT_TIMESTAMP,
  discipline text not null,
  owns_equipment tinyint not null,
  draw_weight int,
  draw_length int,
  equipment_description text,
  distance int,
  joad_day text
);

-- drop table if exists member_data;
-- create table  member_data (
--   id,
--   date date not null,
--   discipline text not null,
--   draweight int,
--   distance int,
--   targetsize int,
--   tournament int,
--   score int,
--   num_arrows int,
--   notes text
-- );
