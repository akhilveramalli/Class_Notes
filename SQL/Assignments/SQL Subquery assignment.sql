-- 1. display all customer details who have made more than 5 payments.

select * from sakila.customer 
where customer_id in (select customer_id from sakila.payment 
group by customer_id having count(*) > 5);

-- 2. Find the names of actors who have acted in more than 10 films.

select first_name, last_name from sakila.actor 
where actor_id in ( select actor_id from sakila.film_actor group by actor_id having count(*) > 10);

-- 3. Find the names of customers who never made a payment.

select * from sakila.customer where customer_id not in (select customer_id from sakila.payment);

-- 4. List all films whose rental rate is higher than the average rental rate of all films.

select title, rental_rate from sakila.film where rental_rate > (select avg(rental_rate) from sakila.film);

-- 5. List the titles of films that were never rented.

select title from sakila.film where film_id not in (
select film_id from sakila.inventory where inventory_id in (select inventory_id from sakila.rental));

-- 6. Display the customers who rented films in the same month as customer with ID 5.

with cust5_months as (
select distinct month(rental_date) as rental_month from sakila.rental where customer_id = 5
)

select distinct c.customer_id, c.first_name, c.last_name  from sakila.customer c
join sakila.rental r on c.customer_id = r.customer_id 
where month(r.rental_date) in (select rental_month from cust5_months) and r.customer_id <> 5;

-- 7. Find all staff members who handled a payment greater than the average payment amount.

with avg_amt as (
select avg(amount) as average_amount from sakila.payment
)

select distinct s.staff_id, s.first_name, s.last_name from sakila.staff s join 
sakila.payment p on s.staff_id = p.staff_id where p.amount > ( select average_amount from avg_amt);

-- 8. Show the title and rental duration of films whose rental duration is greater than the average.
with avg_d as (
select avg(rental_duration) as avg_rental_duration from sakila.film 
)

select title, rental_duration from sakila.film where rental_duration > (select avg_rental_duration from avg_d);

-- 9. Find all customers who have the same address as customer with ID 1.

create temporary table tmp_address as
select address_id from sakila.customer where customer_id = 1;

select customer_id, first_name, last_name from sakila.customer where address_id = (select address_id from tmp_address) and customer_id <> 1;

-- 10. List all payments that are greater than the average of all payments. 

create view avg_payment_view as 
select avg(amount) as average_amount from sakila.payment;

select * from sakila.payment where amount > ( select average_amount from sakila.avg_payment_view);
