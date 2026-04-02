

USE sakila; 

# String Inbuilt Function

-- UPPER()
SELECT first_name, UPPER(first_name) AS upper_name
FROM customer;

-- LOWER()
SELECT last_name, LOWER(last_name) AS lower_name
FROM customer;

-- LENGTH()
SELECT title, LENGTH(title) AS title_length
FROM film;

-- SUBSTRING()
SELECT title, SUBSTRING(title, 1, 5) AS short_title
FROM film;

-- CONCAT()
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM customer;

-- REPLACE()
SELECT title, REPLACE(title, 'A', '@') AS modified_title
FROM film;

-- INSTR()
SELECT title, INSTR(title, 'LOVE') AS position
FROM film;

-- TRIM()
SELECT TRIM('   Sakila Database   ') AS cleaned_text;

-- LTRIM() and RTRIM()
SELECT LTRIM('   Hello') AS left_trim,
       RTRIM('Hello   ') AS right_trim;

-- LPAD()
SELECT first_name, LPAD(first_name, 10, '*') AS padded_name
FROM customer;

-- RPAD()
SELECT first_name, RPAD(first_name, 10, '*') AS padded_name
FROM customer;

-- REVERSE()
SELECT first_name, REVERSE(first_name) AS reversed_name
FROM customer;

-- REPEAT()
SELECT REPEAT('SQL ', 3) AS repeated_text;

-- ASCII()
SELECT first_name, ASCII(first_name) AS ascii_value
FROM customer;

-- CHAR()
SELECT CHAR(65, 66, 67) AS characters;

-- LEFT()
SELECT title, LEFT(title, 4) AS first_part
FROM film;

-- RIGHT()
SELECT title, RIGHT(title, 4) AS last_part
FROM film;

-- LIKE
SELECT first_name
FROM customer
WHERE first_name LIKE 'A%';

-- REGEXP
SELECT first_name
FROM customer
WHERE first_name REGEXP '^(A|B)';



# Numeric Functions

-- ABS() - absolute value
SELECT amount, ABS(amount - 5) AS absolute_value
FROM payment
LIMIT 5;

-- CEIL() / CEILING() - smallest integer >= amount
SELECT amount, CEIL(amount) AS ceil_value
FROM payment
LIMIT 5;

-- FLOOR() - largest integer <= amount
SELECT amount, FLOOR(amount) AS floor_value
FROM payment
LIMIT 5;

-- ROUND() - round to nearest integer or decimals
SELECT amount, 
       ROUND(amount) AS rounded_integer,
       ROUND(amount, 1) AS rounded_one_decimal,
       ROUND(amount, 2) AS rounded_two_decimals
FROM payment
LIMIT 5;

-- TRUNCATE() - truncate decimals without rounding
SELECT amount, 
       TRUNCATE(amount, 1) AS truncated_one_decimal,
       TRUNCATE(amount, 0) AS truncated_integer
FROM payment
LIMIT 5;

-- POWER() - square the amount
SELECT amount, POWER(amount, 2) AS squared_amount
FROM payment
LIMIT 5;

-- SQRT() - square root of the amount
SELECT amount, SQRT(amount) AS square_root
FROM payment
LIMIT 5;

-- MOD() - remainder after dividing by 2
SELECT amount, MOD(amount, 2) AS modulo_2
FROM payment
LIMIT 5;

-- EXP() -
SELECT amount, EXP(amount) AS exp
FROM payment
LIMIT 5;

-- LOG() - returns the natural logarithm (base e) of a number.
SELECT amount, LOG(amount) AS log_value
FROM payment
LIMIT 5;

-- RAND() - random number for demonstration (e.g., discount simulation)
SELECT amount, amount * RAND() AS random_discount
FROM payment
LIMIT 5;



# Date Functions

-- NOW()
SELECT payment_date, NOW() AS current_datetime
FROM payment
LIMIT 5;

-- CURDATE()
SELECT payment_date, CURDATE() AS todays_date
FROM payment
LIMIT 5;

-- CURTIME()
SELECT payment_date, CURTIME() AS cur_time
FROM payment
LIMIT 5;

-- DATE()
SELECT payment_date, DATE(payment_date) AS date_only
FROM payment
LIMIT 5;

-- EXTRACT() – extract specific parts (year, month, day)
SELECT 
    payment_date,
    EXTRACT(YEAR FROM payment_date) AS year_part,
    EXTRACT(MONTH FROM payment_date) AS month_part,
    EXTRACT(DAY FROM payment_date) AS day_part
FROM payment
LIMIT 5;

-- DATE_ADD() – add an interval (e.g., 7 days)
SELECT payment_date,
       DATE_ADD(payment_date, INTERVAL 7 DAY) AS plus_7_days
FROM payment
LIMIT 5;

-- DATEDIFF() – difference in days between two dates
SELECT payment_date,
       DATEDIFF(NOW(), payment_date) AS days_since_payment
FROM payment
LIMIT 5;

-- DATE_FORMAT() – format date output
SELECT payment_date,
       DATE_FORMAT(payment_date, '%W, %M %d, %Y') AS formatted_date
FROM payment
LIMIT 5;


# Conditional logic using case

SELECT payment_id, amount,
       CASE 
           WHEN amount < 3 THEN 'Small'
           WHEN amount BETWEEN 3 AND 7 THEN 'Medium'
           ELSE 'Large'
       END AS payment_category
FROM payment
LIMIT 10;



