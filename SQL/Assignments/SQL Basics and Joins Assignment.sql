# sql basics

USE sakila;

# 1. Get all customers whose first name starts with 'J' and who are active.
select * from customer where first_name like 'J%' and active = 1;

# 2. Find all films where the title contains the word 'ACTION' or the description contains 'WAR'.
select * from film where title like '%ACTION%' or description like '%WAR%';

# 3. List all customers whose last name is not 'SMITH' and whose first name ends with 'a'.
select * from customer where last_name <> 'SMITH' and first_name like '%a';

# 4. Get all films where the rental rate is greater than 3.0 and the replacement cost is not null.
select title, rental_rate, replacement_cost from film where rental_rate > 3 and replacement_cost is not Null ;

# 5. Count how many customers exist in each store who have active status = 1.
select store_id, count(customer_id) from customer where active = 1 group by store_id;

# 6. Show distinct film ratings available in the film table.
select distinct rating from film as Distinct_Ratings;

# 7. Find the number of films for each rental duration where the average length is more than 100 minutes.
select rental_duration, count(*) from film where length > 100 group by rental_duration;

# 8. List payment dates and total amount paid per date, but only include days where more than 100 payments were made.
select payment_date, count(payment_id) as count_of_payments from payment group by payment_date  having count(payment_id) > 100;

# 9. Find customers whose email address is null or ends with '.org'.
select email from customer where email is null or email like '%.org' ;

# 10. List all films with rating 'PG' or 'G', and order them by rental rate in descending order.
select title, rating, rental_rate  from film where rating in ('PG', 'G') order by rental_rate desc;

# 11. Count how many films exist for each length where the film title starts with 'T' and the count is more than 5.
select length, count(*) from film where title like 'T%' group by length having count(*) < 5;

# 12. List all actors who have appeared in more than 10 films.
select actor_id, count(film_id) as Film_Count from film_actor group by actor_id having count(film_id) > 10 ;

# 13. Find the top 5 films with the highest rental rates and longest lengths combined, ordering by rental rate first and length second.
select title, rental_rate, length from film order by rental_rate desc, length desc limit 5;

# 14. Show all customers along with the total number of rentals they have made, ordered from most to least rentals.
select customer_id, count(customer_id) as Rental_Count from rental group by customer_id order by count(customer_id) desc ;

# 15. List the film titles that have never been rented.
select f.title from film f 
left join inventory i on f.film_id = i.film_id
left join rental r on i.inventory_id = r.inventory_id
where r.rental_id is null;


# SQL Joins

# 1. List all customers along with the films they have rented.
select c.customer_id, c.first_name, c.last_name, f.title from customer c 
left join rental r on c.customer_id=r.customer_id
left join inventory i on r.inventory_id = i.inventory_id
left join film f on i.film_id = f.film_id ;
 

# 2. List all customers and show their rental count, including those who haven't rented any films.
select c.first_name, c.last_name, count(r.rental_id) as rental_count from customer c
left join rental r on c.customer_id = r.customer_id
group by c.customer_id;


# 3. Show all films along with their category. Include films that don't have a category assigned.
select f.title, c.name from film f
left join film_category fc on f.film_id = fc.film_id
left join category c on fc.category_id = c.category_id;


# 4. Show all customers and staff emails from both customer and staff tables using a full outer join (simulate using LEFT + RIGHT + UNION).
-- LEFT JOIN part
SELECT c.email AS email
FROM customer c
LEFT JOIN staff s ON c.email = s.email

UNION

-- RIGHT JOIN part
SELECT s.email AS email
FROM customer c
RIGHT JOIN staff s ON c.email = s.email;


# 5. Find all actors who acted in the film "ACADEMY DINOSAUR".
select a.first_name, a.last_name, f.title from film f
inner join  film_actor fa on f.film_id = fa.film_id
inner join actor a on fa.actor_id = a.actor_id
where f.title = "ACADEMY DINOSAUR";

# 6. List all stores and the total number of staff members working in each store, even if a store has no staff.
select s.store_id, count(st.staff_id) from store s
left join staff st on s.store_id = st.store_id
group by s.store_id;

# 7. List the customers who have rented films more than 5 times. Include their name and total rental count.
select c.first_name, c.last_name, count(r.rental_id) as Rental_Count from customer c
inner join rental r on c.customer_id = r.customer_id 
group by c.customer_id
having count(r.rental_id) > 5;
