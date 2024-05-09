
-----------------------------------------------------------------------
i)
--Retrieves All tweet text (Newest to Oldest)(LIMIT 5 not implemented yet)
SELECT t.text 
FROM tweets t
ORDER BY tdate ASC


--Retrieves All hashtag terms
SELECT h.term
FROM hashtags h

--Retrieves All DISTINCT mention terms
SELECT DISTINCT m.term
FROM mentions m

-------------------------------------------------------------------------
ii)
--Number of retweets (Selected tweet)
SELECT r.tid, COUNT(r.usr)
FROM retweets r
WHERE r.tid = ?

--Number of replies to a tweet (Selected tweet)
SELECT t.replyto, COUNT(*) as Number_of_replies
FROM tweets t
WHERE t.replyto = ?
GROUP BY t.replyto


-- iii) checks reply to a tweet #3 specification
--------------------------------------------------------------------------
iv) 
INSERT INTO retweets (usr, tid, rdate) 
VALUES (?, ?, DATE(?))


-------------------------------------------------------------------------






















SELECT r.writer, r.tdate, COUNT(r.usr) as num_
FROM retweets r
WHERE r.writer = 101 AND r.tdate = '2023-02-16'
--GROUP BY r.writer, r.tdate






SELECT *
FROM tweets t
ORDER BY tdate ASC


SELECT t.replyto_w, t.replyto_d, COUNT(*) as Number_of_replies
FROM tweets t
WHERE t.replyto_w IS NOT NULL AND t.replyto_d IS NOT NULL
GROUP BY t.replyto_w, t.replyto_d