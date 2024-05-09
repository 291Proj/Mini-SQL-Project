

----------------------------------------------------
i)
--users that follow him
SELECT u.name, f.flwer 
FROM follows f
JOIN users u ON u.usr = f.flwer
WHERE f.flwee = ?



----------------------------------------------------
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



--------------------------------------------------
iii)
--option to follow the selected user
INSERT INTO follows (flwee, flwer, start_date)
VALUES (?, ?, ?);

/*
current_date = datetime.now().date()

# Insert the date into the table
cursor.execute("INSERT INTO my_table (date_column) VALUES (?)", (current_date,))
conn.commit()
*/

----------------------------------------------------















































SELECT flwee, flwer
FROM follows
ORDER BY flwee ASC
--GROUP BY flwee


SELECT u.name AS Name, f.flwee AS ID, COUNT(f.flwer) AS Total_Followers
From users u
JOIN follows f ON u.usr = f.flwee
GROUP BY u.name 
ORDER BY flwee ASC
--LIMIT 2


SELECT u.name, f.flwee AS ID, COUNT(f.flwer) AS total_followers
From users u
JOIN follows f ON u.usr = f.flwee
WHERE flwee = 1 
GROUP BY u.name 
ORDER BY flwee ASC
--LIMIT 2



SELECT u.name, f.flwee, 
FROM users u
JOIN follows f ON u.usr = f.flwee
--WHERE flwee = 1
--GROUP BY u.name 
--ORDER BY flwee ASC


SELECT u.name, f.flwer 
FROM follows f
JOIN users u ON u.usr = f.flwer
WHERE f.flwee = 2



SELECT u.name, COUNT(f.flwee) AS Total_people_following
FROM users u
JOIN follows f ON u.usr = f.flwer
WHERE flwer = 1
GROUP BY u.name
ORDER BY flwer ASC


SELECT u.name, t.writer AS ID, COUNT(t.text) AS Number_of_Tweets
FROM tweets t
JOIN users u ON u.usr = t.writer
WHERE t.writer = 5
GROUP BY t.writer
ORDER BY t.writer 



SELECT *
FROM tweets t
WHERE t.writer = 5
ORDER BY t.tdate 
LIMIT 3