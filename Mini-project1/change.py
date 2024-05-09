
import sqlite3
import datetime
# Global variables
connection = None
cursor = None

def connect(path):
    '''Conects to the database specified by the user'''
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()

    return











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







































def main():
    global connection, cursor

    path = "test1.db"
    connect(path)

    '''
    a_list = tweet_search('j')

    if a_list == False:
        print ('No keyword found')
    else:
        for i in a_list:
            print(i[0])

    '''
    insert_tweet(0, 'Hello #akib you #yuna', None)







    connection.commit()
    connection.close()
    return





if __name__ == "__main__":
    main()













'''



    



'''