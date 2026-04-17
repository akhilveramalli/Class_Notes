Create database testdb;
show databases;
use testdb;

CREATE TABLE Persons (
  PersonID int PRIMARY KEY,
  LastName varchar(255) NOT NULL,
  FirstName varchar(255),
  Address varchar(255),
  City varchar(255)
);

INSERT INTO Persons (PersonID, LastName, FirstName, Address, City)
VALUES
(1, 'Wilson', 'Chris', '159 Elm Street', 'San Antonio'),
(2, 'Moore', 'Patricia', '753 Willow Way', 'San Diego'),
(3, 'Taylor', 'James', '852 Aspen Court', 'Dallas');

INSERT INTO Persons (PersonID, LastName, FirstName, Address, City)
VALUES
(7, 'Williams', 'Jacob', '305 stam dr', 'San Antonio'),
(6, 'Ward', 'rashod', '203 guthire ct', 'San Diego'),
(5, 'Ward', 'jhon', '155 james ct', 'Dallas');
select * from Persons;
-- single line comments

/* Multi line
comments
 */
 
 -- Alias and Concat
SELECT CONCAT(FirstName, ' ', LastName) AS FullName FROM PERSONS;
--   select field("chris", FirstName) from persons;

-- where Null
select * from persons where city is Null;

-- distinct group by
select distinct City, count(city) from Persons group by City;

select * from persons order by city;


--  limit
SELECT * FROM persons limit 3;
SELECT * FROM persons limit 1;

-- Pattern matching with like

select * from persons where City like 'San%'; -- City starting with San
select * from persons where Address like '%ct'; -- Address ending with ct
select * from persons where FirstName like '%sh%'; -- FirstName contains Pattern with sh


ALTER TABLE Persons
ADD Age int;
select * from persons;



select count(*) from persons;

select sum(Age) as SumOfAge, Avg(Age) as AverageAge, Min(Age) as MinimumAge, Max(age) as MaximumAge from persons;



-- String Function

-- CHAR_LENGTH

SELECT FirstName, CHAR_LENGTH(FirstName) AS LengthOfName FROM persons;


-- CONCAT

SELECT CONCAT(FirstName, ' ', LastName) AS FullName FROM PERSONS;

-- CONCAT_WS

SELECT CONCAT_WS(' ',FirstName, LastName) AS FullName FROM PERSONS;

-- FIELD(): The function returns the index position of a value in a list of values.

SELECT FIELD("q", "s", "q", "l");
select * from persons;

-- Format the number as "#,###,###.##" (and round with two decimal places):

SELECT FORMAT(250500.5634, 2);

-- Insert the string "Example" into the string "W3Schools.com". Replace the first nine characters:

SELECT INSERT("W3Schools.com", 1, 9, "Example");


-- The INSTR() function returns the position of the first occurrence of a string in another string.

SELECT INSTR("W3Schools.com", "3") AS MatchPosition;

-- LCASE & LOWER Convert the text to lower-case:

SELECT LCASE("SQL Tutorial is FUN!");

SELECT LOWER("SQL Tutorial is FUN!");

-- UPASE & UPPER Convert the text to upper-case:

SELECT UCASE("SQL Tutorial is FUN!");

-- LEFT : Extract a number of characters from a string (starting from left):

SELECT LEFT("SQL Tutorial", 3) AS ExtractString;

-- Length

SELECT LENGTH("SQL Tutorial") AS LengthOfString;

-- The LOCATE() function returns the position of the first occurrence of a substring in a string.

SELECT LOCATE("3", "W3Schools.com") AS MatchPosition;

-- The LPAD() function left-pads a string with another string, to a certain length.

SELECT LPAD("SQL Tutorial", 20, "ABC");

-- The RPAD() function right-pads a string with another string, to a certain length.

SELECT RPAD("SQL Tutorial", 20, "ABC");

-- The RTRIM() function removes trailing spaces from a string.

SELECT RTRIM("SQL Tutorial     ") AS RightTrimmedString;

-- The LTRIM() function removes leading spaces from a string.


SELECT LTRIM("     SQL Tutorial") AS LeftTrimmedString;

-- The REPEAT() function repeats a string as many times as specified.

-- SELECT REPEAT("SQl Tutorial", 3);

-- The REPLACE() function replaces all occurrences of a substring within a string, with a new substring.

SELECT REPLACE("SQL Tutorial", "SQL", "HTML");

-- The REVERSE() function reverses a string and returns the result.

SELECT REVERSE("SQL Tutorial");


-- Numeric functions

SELECT ABS(-243.5);  -- 243.5

SELECT CEIL(25.75); -- 26

SELECT CEILING(25.75); -- 26

SELECT FLOOR(25.76); -- 25

SELECT ROUND(135.375, 2); -- 135.38

SELECT TRUNCATE(135.379, 2); -- 135.37

SELECT 10 DIV 5; -- 2

select SUM(Age) as SumOfAge, AVG(Age) as AverageAge, MIN(Age) as MinimumAge, MAX(age) as MaximumAge from persons;

SELECT RAND() ; --  returns a random number between 0 (inclusive) and 1 (exclusive).

SELECT POWER(4, 2); -- 16
SELECT POW(4, 2); -- 16

SELECT SQRT(64); -- 8


-- DATE FUNCTIONS

SELECT ADDDATE("2017-06-15", INTERVAL 10 DAY); -- The ADDDATE() function adds a time/date interval to a date and then returns the date.
SELECT ADDDATE("2017-06-15 09:34:21", INTERVAL 15 MINUTE);

SELECT ADDTIME("2017-06-15 09:34:21", "2"); -- The ADDTIME() function adds a time interval to a time/datetime and then returns the time/datetime.

SELECT CURDATE();
SELECT CURRENT_DATE();

SELECT CURTIME();
SELECT CURRENT_TIME(); 

SELECT CURRENT_TIMESTAMP();

SELECT DATE("2017-06-15 09:34:21"); -- The DATE() function extracts the date part from a datetime expression.

SELECT DATEDIFF("2017-06-25", "2017-06-15"); -- Return the number of days between two date values:

-- The DATE_FORMAT() function formats a date as specified.

SELECT DATE_FORMAT("2017-06-15", "%Y"); -- 2017
SELECT DATE_FORMAT("2017-06-15", "%a"); -- Thu
SELECT DATE_FORMAT("2017-06-15", "%b"); -- Jun
SELECT DATE_FORMAT("2017-06-15", "%c"); -- 6 Month
SELECT DATE_FORMAT("2017-06-15", "%D"); -- 15th
SELECT DATE_FORMAT("2017-06-9", "%d"); -- 09  (01 - 31)
SELECT DATE_FORMAT("2017-06-9", "%e"); -- 9 (0 - 31)
SELECT DATE_FORMAT("2017-06-15", "%f"); -- 0000 microsecond

/*
%H	Hour (00 to 23)
%h	Hour (00 to 12)
%I	Hour (00 to 12)
%i	Minutes (00 to 59)
%j	Day of the year (001 to 366)
%k	Hour (0 to 23)
%l	Hour (1 to 12)
%M	Month name in full (January to December)
%m	Month name as a numeric value (00 to 12)
%p	AM or PM
%r	Time in 12 hour AM or PM format (hh:mm:ss AM/PM)
%S	Seconds (00 to 59)
%s	Seconds (00 to 59)
%T	Time in 24 hour format (hh:mm:ss)
%U	Week where Sunday is the first day of the week (00 to 53)
%u	Week where Monday is the first day of the week (00 to 53)
%V	Week where Sunday is the first day of the week (01 to 53). Used with %X
%v	Week where Monday is the first day of the week (01 to 53). Used with %x
%W	Weekday name in full (Sunday to Saturday)
%w	Day of the week where Sunday=0 and Saturday=6
%X	Year for the week where Sunday is the first day of the week. Used with %V
%x	Year for the week where Monday is the first day of the week. Used with %v
%Y	Year as a numeric, 4-digit value
%y	Year as a numeric, 2-digit value
*/







