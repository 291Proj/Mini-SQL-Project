import sqlite3
import datetime


############################################################################################################
#
#    READ ME ! ! ! ! ! ! !
#
#   1. Insert and use any parameter that you see fit but let me know if you do so
#   2. If you have questions regarding the implementation of the funstions then ask me (AKIB)
#   3. Functions starting with 'insert' and 'number' are the easiest
#   4. All the functions are divided into 5 parts corresponding to the 5 specifications
#   5. READ the assignment specifications part carefully
#   6. Check the sql files provided to see which sql statements to use
#
##############################################################################################################

# Global variables
connection = None
cursor = None

# Connect to database
def connect(path):
    '''Conects to the database specified by the user'''
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()

    return



















#1 (Done)

def tweet_search(keywords):
    '''searched for tweets using the keyword provided by the user'''
    global connection, cursor

    cursor.execute(
        '''
        SELECT t.text, t.tid 
        FROM tweets t
        ORDER BY tdate ASC
        '''
    )

    total_tweets_list = cursor.fetchall() # [(text, tid),.....]
    connection.commit()



    if keywords[0] == '#':
        a_list = hashtag_checker(total_tweets_list, keywords)

    else:
        a_list = normal_text_checker(total_tweets_list, keywords)

    # IF no tweets match the keyword it returns false
    if a_list == [] :
        return False
    else:
        return a_list




def hashtag_checker(total_tweets_list, keywords):
    '''Checks if the keyword is present in the mentions table (EXACT MATCH)'''
    global connection, cursor

    cursor.execute('''SELECT * FROM mentions''')
    mentions_list = cursor.fetchall() # [( tid, term),.....]

    a_list = []


    for item in mentions_list:
        if (item[1] == keywords[1:]): # checks if term is the same as keyword
            for tweet in total_tweets_list:
                if (tweet[1] == item[0]): # checks if tweet tid is the same mention tid
                    a_list.append((tweet[0], tweet[1]))


    connection.commit()
    return a_list



def normal_text_checker(total_tweets_list, keywords):
    '''Searches for all tweets with the keyword (PARTIAL MATCH)'''
    global connection, cursor

    a_list = []

    for tweet in total_tweets_list:
        if keywords.lower() in tweet[0].lower():
            a_list.append((tweet[0], tweet[1]))

    connection.commit()
    return a_list


def number_of_retweets(tid):
    '''Calculates and returns the number of retweets of the selected tweet'''
    global connection, cursor

    cursor.execute(
        '''
    SELECT r.tid, COUNT(r.usr)
    FROM retweets r
    WHERE r.tid = ?
        ''', (tid,)
    )
    num_retweets = cursor.fetchall() # List of one tuple 
    connection.commit()

    return num_retweets[0][-1]



def number_of_replies(tid):
    '''Calculates and returns the number of replies of the selected tweet'''
    global connection, cursor

    cursor.execute(
        '''
        SELECT t.replyto, COUNT(*) as Number_of_replies
        FROM tweets t
        WHERE t.replyto = ? 
        GROUP BY t.replyto
        ''', (tid,)
    )
    num_replies = cursor.fetchall() # list of replies
    connection.commit()

    if num_replies == []:
        return 0
    else:
        return num_replies[0][-1]



def insert_retweets(usr, tid):
    '''inserts a retweet into the retweets table'''

    global connection, cursor
 
    today = datetime.datetime.today() # Get today's date
    rdate = today.strftime("%Y-%m-%d") # Format the date as "YYYY-MM-DD"


    try:
        cursor.execute('''INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, DATE(?))
                        ''', (int(usr), int(tid), rdate))
        connection.commit()

    except:
        return False

    return rdate

























#2 (Done)
def users_search(keyword):
    '''Searches for user using the keyword provided'''

    #keyword = input("Search for users here: ")
    name_list = name_keyword(keyword)
    city_list = city_keyword(keyword)

    combined_list = name_list + city_list

    return combined_list



def name_keyword(keyword):
    '''Checks for keyword in name (ASCENDING order LEN(name))'''
    global connection, cursor

    cursor.execute(
        '''
        SELECT u.name, u.usr, u.city
        FROM users u
        WHERE u.name LIKE ?
        ORDER BY LENGTH(u.name) ASC
        ''' , ('%' + keyword + '%',)
    )

    matched_users = cursor.fetchall()
    sorted_names = sorted(matched_users, key=lambda x: len(x[0]))
    connection.commit()

    return sorted_names



def city_keyword(keyword):
    '''Checks for keyword in city (ASCENDING order LEN(city))'''
    global connection, cursor

    cursor.execute(
        '''
        SELECT c.name, c.usr, c.city
        FROM users c
        WHERE c.city LIKE ?
        AND c.name NOT LIKE ?
        ORDER BY LENGTH(c.city) ASC
        ''' , ('%' + keyword + '%','%' + keyword + '%',)
    )
    matched_cities = cursor.fetchall()
    sorted_cities = sorted(matched_cities, key=lambda x: len(x[0]))
    connection.commit()

    return sorted_cities






















#3 (Done)

def insert_tweet(writer, text, replyto): 
    '''inserts a tweet into the tweets table'''
    global connection, cursor

    today = datetime.datetime.today() # Get today's date  
    tdate = today.strftime("%Y-%m-%d") # Format the date as "YYYY-MM-DD"
    

    cursor.execute('''SELECT DISTINCT t.tid FROM tweets t''')
    a_list = cursor.fetchall() # a list of tuble containing the tid
    b_list = [] #empty list where we will insert the int tid values

    for item in a_list:
        b_list.append(int(item[0]))

    tid = max(b_list) + 1

    try:
        cursor.execute('''INSERT INTO tweets (tid, writer, tdate, text, replyto)
                    VALUES (?, ?, DATE(?), ?, ?)
                    ''', (tid, writer, tdate, text, replyto))
        connection.commit()
    except:
        return False
    
    # Split the input sentence into words
    words = text.split()
    # stores hashtag terms in a list
    hashtag_terms = [word[1:] for word in words if word.startswith("#")]

    for hashtag in hashtag_terms:
        insert_hashtags(hashtag)
        insert_mentions(tid, hashtag)

    return tdate



def insert_hashtags(hashtag):
    '''inserts a hashtag into the hashtag table'''
    global connection, cursor
    
    try:
        cursor.execute('''INSERT INTO hashtags (term)
                    VALUES (?)
                    ''', (hashtag,))
        connection.commit()
    except:
        return False

    return



def insert_mentions(tweet_id, hashtag):
    '''inserts a mention into the mentions table'''
    global connection, cursor
    
    try:
        cursor.execute('''INSERT INTO mentions (tid, term)
                    VALUES (?, ?)
                    ''', (tweet_id, hashtag))
        connection.commit()
    except:
        return False

    return





















#4 (Done)

def followers_list(user_id):
    '''Lists all the users that follow the logged in user
    returns list of tuples (usr, name)'''
    global connection, cursor
    cursor.execute(
        '''
        SELECT u.name, u.usr 
        FROM follows f
        JOIN users u ON u.usr = f.flwer
        WHERE f.flwee = ?;
        ''' , (user_id,)
    )
    matched_followers = cursor.fetchall()

    a_list = []
    #inserts only user names into the list
    for item in matched_followers:
        a_list.append((item[1], item[0]))

    connection.commit()
    return a_list

def number_of_tweets(user_id):
    '''Calculates and returns the number of tweets of the selected user'''
    global connection, cursor
    cursor.execute(
        '''
        SELECT u.name, t.writer AS ID, COUNT(t.text) AS Number_of_Tweets_posted
        FROM tweets t
        JOIN users u ON u.usr = t.writer
        WHERE t.writer = ?
        GROUP BY t.writer
        ORDER BY t.writer; 
        ''' , (user_id,)
    )
    matched_tweets = cursor.fetchall()
    if matched_tweets == []:
        return 0
    
    connection.commit()
    return matched_tweets[0][2]



def number_of_followers(user_id):
    '''Calculates and returns the number of followers of the selected user'''
    global connection, cursor
    cursor.execute(
        '''
        SELECT u.name AS Name, f.flwee AS ID, COUNT(f.flwer) AS Total_Followers
        From users u
        JOIN follows f ON u.usr = f.flwee
        WHERE flwee = ?
        GROUP BY u.name 
        ORDER BY flwee ASC;
        ''' , (user_id,)
    )
    matched_followers = cursor.fetchall()
    if matched_followers == []:
        return 0
    
    connection.commit()
    return matched_followers[0][2]



def number_of_following(user_id):
    '''Calculates and returns the number of replies of the selected user'''
    global connection, cursor
    cursor.execute(
        '''
        SELECT u.name, COUNT(f.flwee) AS Total_people_following
        FROM users u
        JOIN follows f ON u.usr = f.flwer
        WHERE flwer = ?
        GROUP BY u.name
        ORDER BY flwer ASC; 
        ''' , (user_id,)
    )
    matched_followees = cursor.fetchall()
    if matched_followees == []:
        return 0
    
    connection.commit()
    return matched_followees[0][1]



def recent_tweets(user_id):
    '''shows recent tweets of the selected user (LIMITED TO 3)'''
    global connection, cursor
    cursor.execute(
        '''
        SELECT *
        FROM tweets t
        WHERE t.writer = ?
        ORDER BY t.tdate; 
        ''' , (user_id,)
    )
    matched_tweets = cursor.fetchall()
    connection.commit()

    if matched_tweets == []:
        return False
    else:
        return matched_tweets


#parameter takes either a list or a tuple
def insert_follows(flwee, flwer):
    '''Inserts a follow into the follows table'''
    global connection, cursor
    cursor.execute(
        '''
        SELECT * 
        FROM follows
        WHERE follows.flwee = ? AND follows.flwer = ?
        ''', (flwee, flwer)
    )
    exists = cursor.fetchone()
    if not exists is None:
        return False

    today = datetime.datetime.today() # Get today's date
    start_date = today.strftime("%Y-%m-%d") # Format the date as "YYYY-MM-DD"
    cursor.execute(
        '''
        INSERT INTO follows 
        VALUES (?, ?, ?); 
        ''' , (flwer, flwee, start_date,)
    )
    connection.commit()
    return True




















#5 (NOT DONE)


def logout_():
    '''
    There must be an option to log out of the system. 
    '''

    connection.close()
    return
























#6 (NOT DONE)


def validate_user_login(user_id, password):
    '''validates user ID and passwords with existing data'''
    # returns 1 if valid login
    # returns 0 if invalid login
    global connection, cursor

    cursor.execute(
        '''
        SELECT users.usr as ID, users.pwd as password
        FROM users
        WHERE users.usr = ?
        ''', (user_id,)
    )
    user_and_password = cursor.fetchall()
    connection.commit()
    if user_and_password == []:
        return False
    elif user_and_password[0][1] != password:
        return False
    else:
        return True




def user_signup(password, name, email ,city, timezone):
    '''insert new data in users table to register new user'''
    global connection, cursor

    cursor.execute(
        '''
        SELECT MAX(users.usr) 
        FROM users
        ''' )

    max_id = cursor.fetchone() 
    max_id = max_id[0]
    if max_id is None:
        max_id = 0
    new_id = int(max_id) + 1
    new_record = (new_id, password, name, email ,city, timezone)
    
    try:
        cursor.execute(
            '''
            INSERT INTO users
            VALUES (?, ?, ?, ?, ?, ?)
            ''', new_record 
        )
        connection.commit()
    except:
        return False
    return new_id





def find_user_name(user_id):
    '''finds user name from user ID'''
    # returns name if user_id exists
    # returns None if user_id does not exist
    global connection, cursor

    cursor.execute(
        '''
        SELECT users.name as name
        FROM users
        WHERE users.usr = ?
        ''', (user_id,)
    )
    name = cursor.fetchone() 
    if name is None:
        return None
    name = name[0]

    connection.commit()
    return name


def user_feed_posts(user_id):
    '''finds all tweets and retweets from followees in descending order ot date
    returns list of tuples (R/T, tid, user, date, text)
    the list is sorted by the date in descending order'''

    global connection, cursor
    cursor.execute(
        '''
        SELECT t.tid, t.writer, t.tdate, t.text, r.usr, r.rdate
        FROM tweets t
        LEFT JOIN retweets r ON t.tid = r.tid
        WHERE r.usr IN
            (
                SELECT follows.flwee
                FROM follows
                WHERE follows.flwer = ?
            )
            OR t.writer IN 
            (
                SELECT follows.flwee
                FROM follows
                WHERE follows.flwer = ?
            )
        ''', (user_id, user_id)
    )
    connection.commit()
    tweet_list = cursor.fetchall()  #list of tuples containing usr of followees
    for index in range(0, len(tweet_list)):
        if not tweet_list[index][4] is None:  #is a retweet
            x = tweet_list[index]
            tweet_list[index] = ('Retweet', x[0], x[4], x[5], x[3])
        else:  #is an original tweet
            x = tweet_list[index]
            tweet_list[index] = ('Tweet', x[0], x[1], x[2], x[3])

    tweet_list = sorted(tweet_list, key=lambda x: x[3], reverse = True)
    return tweet_list