
-- SUBQUERIES - DRAWBACKS
-- Complexity:  Hard to read and debug due to multiple nesting levels
-- Scope Issue: Subqueries exist only within the query they are written in and Cannot reuse this logic elsewhere
-- No Reusability: If same logic is needed again, we must rewrite the subquery



#### CTE (Common Table Expression)

-- CTE improves readability and reduces complexity
-- Easier to read compared to nested subqueries
-- Can reuse 'rental_count' inside the same query

-- Limitation:
-- Scope is still limited to this query only
-- Cannot use 'rental_count' outside this query

WITH rental_count AS (
    SELECT customer_id, COUNT(*) AS total_rentals
    FROM rental
    GROUP BY customer_id
)
SELECT *
FROM rental_count
WHERE total_rentals > 30;



#### RECURSIVE CTE

-- Recursive CTE generates sequence using self-reference
WITH RECURSIVE numbers AS (
    SELECT 1 AS n        -- Anchor (starting point)

    UNION ALL

    SELECT n + 2         -- Recursive step
    FROM numbers
    WHERE n < 20         -- Termination condition
)
SELECT * FROM numbers;





#### TEMPORARY TABLES

-- Temporary table exists only during the session
-- Scope: Session-level (available until session ends)
-- Can reuse this table multiple times during the current session

CREATE TEMPORARY TABLE temp_rentals AS
SELECT customer_id, COUNT(*) AS total_rentals
FROM rental
GROUP BY customer_id;

SELECT * FROM temp_rentals;


#### VIEWS

-- View is a virtual table (stores query, not data)
-- Scope: Database-level (permanent until dropped)
-- Improves reusability and abstraction - hiding sensitive data and renaming columns according to the need
-- Data is NOT stored physically
-- Query runs every time the view is accessed

CREATE VIEW customer_rentals AS
SELECT c.customer_id, c.first_name, COUNT(r.rental_id) AS total_rentals
FROM customer c
LEFT JOIN rental r 
ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name;

SELECT * FROM customer_rentals;





