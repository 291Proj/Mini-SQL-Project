
-------------------------------------------
i) 

--Users composes a tweet
INSERT INTO tweets (tid, writer, tdate, text, replyto) 
VALUES (?, ?, DATE(?), ?, ?)

--If tweets has new hashtag it gets inserted in hashtags table
INSERT INTO hashtags (term)
VALUES (?)

--If tweet mentions a hashtag it gets inserted into mentions table
INSERT INTO mentions (tid, term)
VALUES (?, ?)


-------------------------------------------------------
















SELECT t.replyto, COUNT(*) as Number_of_replies
FROM tweets t
WHERE t.replyto = 27
GROUP BY t.replyto
 






SELECT t.text, t.tid 
FROM tweets t
WHERE t.text LIKE '%j%'
ORDER BY tdate ASC












SELECT DISTINCT u.usr
FROM users u







SELECT DISTINCT h.term, COUNT(m.term)
FROM mentions m
JOIN hashtags h ON h.term = m.term
GROUP BY m.term
HAVING COUNT(m.term) >= 2
ORDER BY COUNT(m.term) ASC