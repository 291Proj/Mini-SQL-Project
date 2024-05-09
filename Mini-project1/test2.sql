
--------------------------------------------------
i)
--Matches user name (ASC LENGTH)
SELECT u.name, u.usr, u.city
FROM users u
WHERE u.name LIKE '%?%'
ORDER BY LENGTH(u.name) ASC

----Matches user city (ASC LENGTH)
SELECT c.name, c.usr, c.city
FROM users c
WHERE c.city LIKE '%?%'
AND c.name NOT LIKE '%?%'
ORDER BY LENGTH(c.city) ASC

--LIMITED TO 5 USERS (option to see more users not implemented yet)


--------------------------------------------------
ii)
--number of tweets of the selecter user
SELECT u.name, t.writer AS ID, COUNT(t.text) AS Number_of_Tweets_posted
FROM tweets t
JOIN users u ON u.usr = t.writer
WHERE t.writer = ?
GROUP BY t.writer
ORDER BY t.writer 

--number of followers of the selected user
SELECT u.name AS Name, f.flwee AS ID, COUNT(f.flwer) AS Total_Followers
From users u
JOIN follows f ON u.usr = f.flwee
WHERE flwee = ?
GROUP BY u.name 
ORDER BY flwee ASC

--number of people the selected user is following
SELECT u.name, COUNT(f.flwee) AS Total_people_following
FROM users u
JOIN follows f ON u.usr = f.flwer
WHERE flwer = ?
GROUP BY u.name
ORDER BY flwer ASC

--3 most recent tweets (option to see more tweets not implemented yet)
SELECT *
FROM tweets t
WHERE t.writer = ?
ORDER BY t.tdate 
LIMIT 3


-----------------------------------------------------------
iii)
--option to follow the selected user
INSERT INTO follows (flwee, flwer, start_date)
VALUES (?, ?, ?);


----------------------------------------------------























SELECT usr, name, city
FROM users
WHERE name LIKE '%oo%'
UNION
SELECT usr, name, city
FROM users
WHERE city LIKE '%keyword'
AND name NOT LIKE '%keyword'
ORDER BY
  CASE
    WHEN name LIKE '%keyword' THEN LENGTH(name)
    ELSE LENGTH(city)
  END,
  name;








SELECT u.name, u.usr, u.city--, LENGTH(name)
FROM users u
WHERE u.name LIKE '%b%'
UNION
SELECT c.name, c.usr, c.city
FROM users c
WHERE c.city LIKE '%b%'
AND c.name NOT LIKE '%b%'
ORDER BY

  CASE
    WHEN u.name LIKE '%b%' THEN LENGTH(u.name)
    ELSE LENGTH(u.city)
  END,
  name;









SELECT name, usr, city, LENGTH(name), LENGTH(city)
FROM users 
WHERE usr IN (
    SELECT u.usr
    FROM users u
    WHERE u.name LIKE '%c%'
    UNION
    SELECT c.usr
    FROM users c
    WHERE c.city LIKE '%c%'
    AND c.name NOT LIKE '%c%'
)
ORDER BY --LENGTH(name)
  CASE
    WHEN (name LIKE 'c%' ) THEN usr
    ELSE LENGTH(city)
  END






SELECT u.name, u.usr, u.city--, LENGTH(u.name), LENGTH(u.city)
FROM users u
WHERE u.name LIKE '%c%'
--ORDER BY LENGTH(u.name) ASC
UNION
SELECT c.name, c.usr, c.city--, LENGTH(c.name), LENGTH(c.city)
FROM users c
WHERE c.city LIKE '%c%'
AND c.name NOT LIKE '%c%'
--ORDER BY LENGTH(u.name) ASC, LENGTH(c.city) DESC


    CASE
        WHEN u.name LIKE '%c%' AND u.city NOT LIKE '%c%'THEN LENGTH(u.name) 
        ELSE LENGTH(c.city) 
    END