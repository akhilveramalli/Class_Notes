create database example;
use example;

create table department(
	dept_id int auto_increment, -- Surrogate Key
    dept_name varchar(100),
    primary key (dept_id)
);

insert into department (dept_name)
values
('HR'),
('ACCOUNTING'),
('IT');

select * from department;

create table employee(
	ssn int,  -- natural key
    first_name varchar(50),
    last_name varchar(50),
    salary int,
    dept_id int,
    primary key (ssn),
    foreign key (dept_id) references department(dept_id)
);

insert into employee (ssn, first_name, last_name, salary, dept_id)
values
('123456789', 'John', 'Doe', 60000, 1),
('987654321', 'Jane', 'Smith', 80000, 2),
('123123123', 'Chrish', 'Ward', 90000, 3);

SELECT 
    *
FROM
    employee;



-- optimization techniques;

-- 1.dont use * always only include required columns

select * from sakila.film;

select title from sakila.film;

-- 2.use where before group by and having

explain select rating, count(*) from sakila.film 
group by rating having rating = 'PG';

explain select rating, count(*) from sakila.film 
where rating = 'PG' group by rating;

-- 3.Use Joins instead of subquery

select first_name , last_name from sakila.actor
where actor_id in (select actor_id from sakila.film_actor where film_id=1);


select first_name , last_name from sakila.actor a
join sakila.film_actor fa on a.actor_id = fa.actor_id
where fa.film_id = 1 ;

-- 4.Avoid functions on indexed columns : Instead of year = 2005 use between 2005-01-01 and 2005-12-31

select * from sakila.rental where year(rental_date) = 	2005;

select * from sakila.rental where rental_date between '2005-01-01' and '2005-12-31';

-- 5.Use Limit effectively



-- 6.Use CTE instead of subquery

-- 7.Use EXPLAIN to understand the query execution plan

-- 8.Use maintenance commands periodically

ANALYZE table sakila.film;

OPTIMIZE table sakila.film;

-- 9. Avoid large offsets in pagination

explain select film_id , title from sakila.film limit 900, 10;

explain select film_id , title from sakila.film where film_id > 900 limit 10;




