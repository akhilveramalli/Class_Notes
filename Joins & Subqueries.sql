# Inner Join
use sakila;

SELECT c.first_name, c.last_name, r.rental_id FROM customer c
INNER JOIN rental r  ON c.customer_id = r.customer_id;

# Left join 
SELECT c.first_name, c.last_name, r.rental_id FROM customer c
LEFT JOIN rental r  ON c.customer_id = r.customer_id;

# Right join
SELECT c.first_name, c.last_name, r.rental_id FROM customer c
RIGHT JOIN rental r  ON c.customer_id = r.customer_id;


# Full Outer join

SELECT c.email FROM customer c
LEFT JOIN staff s ON c.email = s.email
UNION
SELECT s.email FROM customer c
RIGHT JOIN staff s ON c.email = s.email;

# Cross Join

SELECT c.first_name, s.first_name FROM customer c
CROSS JOIN staff s;

# Self Join 

SELECT f1.title, f2.title FROM film f1
JOIN film f2  ON f1.length = f2.length
AND f1.film_id <> f2.film_id;


## Subqueries

SELECT title, rental_rate FROM film
WHERE rental_rate = (SELECT MAX(rental_rate) FROM film);

SELECT first_name, last_name FROM customer
WHERE customer_id IN (SELECT customer_id FROM rental);

# Correlated subquery
SELECT f.title FROM film f
WHERE f.length > (SELECT AVG(length) FROM film WHERE rating = f.rating);



