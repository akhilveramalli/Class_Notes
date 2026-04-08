# Stored Procedure
use sakila;

DELIMITER //
CREATE PROCEDURE get_customer_rentals(IN cust_id INT)
BEGIN
    SELECT *
    FROM rental
    WHERE customer_id = cust_id;
END //

DELIMITER ;

call get_customer_rentals(5);

DELIMITER //
CREATE PROCEDURE get_actor_films(IN actor_id INT)
BEGIN
    select f.title from film f 
	join film_actor fa on f.film_id  = fa.film_id 
	where fa.actor_id = actor_id;
END //

DELIMITER ;

call get_actor_films(1);


DELIMITER //

CREATE PROCEDURE get_rental_count(IN cust_id INT, OUT total INT)
BEGIN
    select COUNT(*) into total
    from rental
    where customer_id = cust_id;
END //

DELIMITER ;

call get_rental_count(1, @count);
select @count;



# clustered index

-- The PRIMARY KEY is automatically the clustered index
-- A table can have ONLY ONE clustered index


select  from film where film_id= 1;


# Non-Clustered Index
-- A table can have MULTIPLE non-clustered indexes

SELECT * FROM film WHERE rental_rate = 2.99;



CREATE INDEX idx_rental_rate ON film(rental_rate);

SELECT * FROM film WHERE rental_rate = 2.99;


CREATE INDEX idx_film_rating ON film(rating);

SELECT * FROM film WHERE rental_rate = 2.99 AND rating = 'PG';



















