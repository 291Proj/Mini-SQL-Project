import backend
import sys

# Global variables
USER_ID = None

# System Functions
def print_box(text, padding=2):
    """Prints a dynamic square box around the given text."""
    max_line_length = max(len(line) for line in text)
    width = max(max_line_length + 2 * padding, 30)
    border = "-" * width
    print(" " + border)
    for line in text:
        left_padding = " " * padding
        right_padding = " " * (width - len(line) - len(left_padding))
        print("|" + left_padding + line + right_padding + "|")
    print(" " + border + "\n")


def display_list(lst, increment):
    """Displays a list of items in an increment. Returns the selected item and its index."""
    if not lst:
        text = ["Your feed is empty."]
        print_box(text)
        return
    current_index = 0
    while True:
        page_items = lst[current_index:current_index + increment]
        text = []
        for i, item in enumerate(page_items, start = 1):
            text.append("{}. {}".format(i, item))

        x = len(lst) / increment
        max_pages = (x > int(x)) + int(x)
        print(f"\nPage {current_index // increment + 1} of {max_pages}", end = "\n") 

        print_box(text)
        text = ["Enter a number to select", "'>' for next page", "'<' for previous page: ", "'C' to Continue."]
        print_box(text)
        choice = input("Enter your choice: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(page_items) :
                return page_items[choice - 1], current_index + choice - 1 
            else:
                text = ["Invalid choice. Please try again!"]
                print_box(text)

        elif choice == '>':
            if current_index + increment < len(lst):
                current_index += increment
            else:
                text = ["End of Page."]
                print_box(text)
        elif choice == '<':
            if current_index > 0:
                current_index -= increment
            else:
                text = ["Beginning of Page."]
                print_box(text)
        elif choice.upper() == 'C':
            return 
        else:
            text = ["Invalid choice. Please try again!"]
            print_box(text)


# Login Screen
def display_login_menu():
    """Displays the login menu."""
    text = ["Welcome to the Twitter!",
            "1. Press 'L' to Login",
            "2. Press 'S' to Sign Up",
            "3. Press 'Q' to Quit"]
    print_box(text)
    choice = input("Enter your choice: ")
    while True:
        if choice.upper() == 'L':
            login()
            return
        elif choice.upper() == 'S':
            sign_up()
            return
        elif choice.upper() == 'Q':
            exit_program()
            return
        else:
            text[0] = "Invalid choice. Please try again!"
            print_box(text)
            choice = input("Enter your choice: ")


def login():
    """login function for the user"""
    global USER_ID
    user_id = input("Enter your User ID: ")
    password = input("Enter your password: ")
    logedin = backend.validate_user_login(user_id, password)
    while True:
        if logedin:
            USER_ID = int(user_id)
            user_name = backend.find_user_name(user_id)
            text = [f'Welcome {user_name}']
            print_box(text)
            display_user_menu()
            False
        else:
            text = ["Invalid User ID or password.",
                    "Please try again."]
            print_box(text)
            login()


def sign_up():
    """sign up function for the user"""
    global USER_ID
    username = input("Enter a new user name: ")
    email = input("Enter your email: ")
    while True:
        if ('@' not in email) or ('.' not in email):
            text = ["Invalid email address.",
                    "Email must have '@' and '.' in it.",
                    "Please try again."]
            print_box(text)
            email = input("Enter your email: ")
        else:
            break
    city = input("Enter your city: ")
    while True:
        if city.isalpha():
            city = city.capitalize()
            break
        else:
            text = ["Invalid city name.",
                    "City name must be alphabetic.",
                    "Please try again."]
            print_box(text)
            city = input("Enter your city: ")
    timezone = input("Enter your timezone: ")
    while True:
        if timezone.isdigit():
            if (-12 <= int(timezone) <= 14):
                break                
            else:
                text = ["Invalid timezone.",
                        "Timezone must be a number between -12 and 14.",
                        "Please try again."]
                print_box(text)
        else:
            text = ["Invalid timezone.",
                    "Timezone must be a number between -12 and 14.",
                    "Please try again."]
            print_box(text)
            timezone = input("Enter your timezone: ")
    password = input("Enter a new password: ")
    user_id = backend.user_signup(password, username, email ,city, timezone)
    text = ["You have successfully signed up!", "Your user ID is: " + str(user_id)]
    USER_ID = user_id
    print_box(text)
    display_user_menu()

def exit_program():
    """exit function for the user"""
    text = ["Are you sure you want to exit?",
            "1. Press Y for Yes",
            "2. Press N for No"]
    print_box(text)
    choice = input("Enter your choice: ")
    if choice.upper() == 'Y':
        text = ["Thank you for using Twitter!",
                "Goodbye!"]
        print_box(text)
        sys.exit()
    elif choice.upper() == 'N':
        display_login_menu()
    else:
        text[0] = "Invalid choice. Please try again!"
        print_box(text)
        choice = input("Enter your choice: ")


# User Interface
def display_user_menu():
    """Displays the main menu for the user along with the feed."""
    global USER_ID
    text = ["Main Menu",
            "1. Press 'S' to search for a tweet",
            "2. Press 'U' to search for a user",
            "3. Press 'P' to post a tweet",
            "4. Press 'L' to open followers list",
            "5. Press 'T' to see your feed",
            "5. Press 'Q' to log out"]
    print_box(text)
    choice = input("Enter your choice: ")
    while True:
        if choice.upper() == 'S':
            search_for_tweets()
            break
        elif choice.upper() == 'U':
            search_for_users()
            break
        elif choice.upper() == 'P':
            post_a_tweets()
            break
        elif choice.upper() == 'L':
            list_followers()
            break
        elif choice.upper() == 'T':

            feed = backend.user_feed_posts(USER_ID)
            for i in range(len(feed)):
                feed[i] = feed[i][4]
            x = display_list(feed, 5)
            if x == None:
                return
            else:
                tweet, tweet_index = x
            if tweet[0].upper() == "RETWEET":
                text = [f"Retweet: {tweet}", "Press 'M' to go to main menu!"]
            else:
                text = [f"Tweet: {tweet}",
                        f"The tweet has {backend.number_of_retweets(tweet[1])} Retweet(s)",
                        f"The tweet has {backend.number_of_replies(tweet[1])} Reply(ies)",
                        f"Do you want to reply to this tweet? Press 'R' to reply",
                        f"Do you want to retweet this tweet? Press 'T' to retweet",
                        f"Press 'M' to go to main menu!"]
            print_box(text)

            choice = input("Enter your choice: ")
            
            while True:
                if choice.upper() == 'R':
                    reply = input("Enter your reply: ")
                    date_time = backend.insert_tweet(USER_ID, reply, tweet[1])
                    text = ["Your reply has been posted!", "Reply: " + reply, "Date: " + date_time]
                    print_box(text)
                    display_user_menu()
                    break
                elif choice.upper() == 'T':
                    date_time = backend.insert_retweets(USER_ID, tweet[1])
                    if date_time == False:
                        text = ["You have already retweeted this tweet!"]
                        print_box(text)
                        display_user_menu()
                        break
                    text = ["Your retweet has been posted!", "Retweet: " + tweet[0], "Date: " + date_time]
                    print_box(text)
                    display_user_menu()
                    break
                elif choice.upper() == 'M':
                    display_user_menu()
                    break
                else:
                    text[0] = "Invalid choice. Please try again!"
                    print_box(text)
                    choice = input("Enter your choice: ")
            break
        elif choice.upper() == 'Q':
            logout_()
            break
        else:
            text[0] = "Invalid choice. Please try again!"
            print_box(text)
            choice = input("Enter your choice: ")
        

def search_for_tweets():
    """Searches for tweets based on a keyword."""
    keyword = input("Enter a keyword: ")
    tweet_list = backend.tweet_search(keyword)
    if tweet_list == False:
        text = ["No tweets found."]
        print_box(text)
        display_user_menu()

    tweet_id = []
    tweet_text =[]

    for i in tweet_list:
        tweet_text.append(i[0])
        tweet_id.append(i[1])
    

    x = display_list(tweet_text, 5)
    if x == None:
        return
    else:
        tweet, tweet_index = x

    if tweet[0].upper() == "RETWEET":
        text = [f"Retweet: {tweet_id[tweet_index]}", "Press 'M' to go to main menu!"]
    else:
        text = [f"Tweet: {tweet_text[tweet_index]}",
                f"The tweet has {backend.number_of_retweets(tweet_id[tweet_index])} Retweet(s)",
                f"The tweet has {backend.number_of_replies(tweet_id[tweet_index])} Reply(ies)",
                f"Do you want to reply to this tweet? Press 'R' to reply",
                f"Do you want to retweet this tweet? Press 'T' to retweet",
                f"Press 'M' to go to main menu!"]
    print_box(text)

    choice = input("Enter your choice: ")
    while True:
        if choice.upper() == 'R':
            reply = input("Enter your reply: ")
            date_time = backend.insert_tweet(USER_ID, reply, tweet_id[tweet_index])
            text = ["Your reply has been posted!", "Reply: " + reply, "Date: " + date_time]
            print_box(text)
            display_user_menu()
            return
        elif choice.upper() == 'T':
            date_time = backend.insert_retweets(USER_ID, tweet_id[tweet_index])
            if date_time == False:
                text = ["You have already retweeted this tweet!"]
                print_box(text)
                display_user_menu()
                return
            text = ["Your retweet has been posted!", "Retweet: " + tweet_text[tweet_index], "Date: " + date_time]
            print_box(text)
            display_user_menu()
            return
        elif choice.upper() == 'M':
            display_user_menu()
            break
        else:
            text[0] = "Invalid choice. Please try again!"
            print_box(text)
            choice = input("Enter your choice: ")



def search_for_users():
    """Searches for users based on a keyword."""
    keyword = input("Enter a keyword: ")
    print_user_list = backend.users_search(keyword)
    user_name_list = []
    user_id_list = []
    user_city_list = []
    for i in print_user_list:
        user_name_list.append(i[0])
        user_id_list.append(i[1])
        user_city_list.append(i[2])

    x = display_list(user_name_list, 5)
    if x == None:
        return
    else:
        list_of_user, index = x

    if list_of_user == False:
        text = ["No users found."]
        print_box(text)
        display_user_menu()
        return

    tweets = backend.recent_tweets(user_id_list[index])
    for i in range(len(tweets)):
        tweets[i] = tweets[i][3]
    numeber_of_tweets = 3
    display_list(tweets, numeber_of_tweets)

    text = [f"You selected user: {user_name_list[index]}",f"From: {user_city_list[index]}",
            f"The user has {backend.number_of_tweets(user_id_list[index])} Tweet(s)",
            f"The user has {backend.number_of_following(user_id_list[index])} Following(s)",
            f"The user has {backend.number_of_followers(user_id_list[index])} Follower(s)",
            f"Do you want to follow this user? Press 'F' to follow",
            f"Press 'M' to go to main menu!"]
    print_box(text)

    choice = input("Enter your choice: ")
    while True:
        if choice.upper() == 'F':
            if USER_ID == user_id_list[index]:
                text = ["You cannot follow yourself!"]
                print_box(text)
                display_user_menu()
                return
            else:
                follow = backend.insert_follows(user_id_list[index], USER_ID)
            if follow:
                text = [f"You are now following {user_name_list[index]}"]
                print_box(text)
                display_user_menu()
            else:
                text = [f"You are already following {user_name_list[index]}"]
                print_box(text)
                display_user_menu()
            return
        elif choice.upper() == 'M':
            display_user_menu()
            return
        else:
            text[0] = "Invalid choice. Please try again!"
            print_box(text)
            choice = input("Enter your choice: ")


def post_a_tweets():
    """Posts a tweet."""
    global USER_ID
    tweet = input("Enter your tweet: ")
    date_time = backend.insert_tweet(USER_ID, tweet, None)
    text = ["Your tweet has been posted!", "Tweet: " + tweet, "Date: " + date_time]
    print_box(text)
    display_user_menu()

def list_followers():
    """Displays the list of followers."""
    global USER_ID
    followers_list = backend.followers_list(USER_ID)
    if followers_list == []:
        text = ["You have no followers."]
        print_box(text)
        display_user_menu()
        return
    
    No_followers = len(followers_list)
    name_list = []
    for i in range (No_followers):
        name_list.append(followers_list[i][1])
    x = display_list(name_list, No_followers)
    if x == None:
        return
    else:
        followers, index = x

    if followers == None:
        display_user_menu()
        return
    follower_id = followers_list[index][0]

    tweets = backend.recent_tweets(follower_id)
    for i in range(len(tweets)):
        tweets[i] = tweets[i][3]

    numeber_of_tweets = 3
    display_list(tweets, numeber_of_tweets)

    text = [f"You selected user: {followers}",
            f"The user has {backend.number_of_tweets(follower_id)} Tweet(s)",
            f"The user has {backend.number_of_following(follower_id)} Following(s)",
            f"The user has {backend.number_of_followers(follower_id)} Follower(s)",
            f"Do you want to follow this user? Press 'F' to follow",
            f"Press 'M' to go to main menu!"]
    print_box(text)

    choice = input("Enter your choice: ")
    while True:
        if choice.upper() == 'F':
            follow = backend.insert_follows(follower_id, USER_ID)
            if follow:
                text = [f"You are now following {followers}"]
                print_box(text)
                display_user_menu()
            else:
                text = [f"You are already following {followers}"]
                print_box(text)
                display_user_menu()
            return
        elif choice.upper() == 'M':
            display_user_menu()
            return
        else:
            text[0] = "Invalid choice. Please try again!"
            print_box(text)
            choice = input("Enter your choice: ")

def logout_():
    """Logs out the user."""
    global USER_ID
    text = ["Are you sure you want to log out?",
            "1. Press Y for Yes",
            "2. Press N for No"]
    print_box(text)
    choice = input("Enter your choice: ")
    if choice.upper() == 'Y':
        display_login_menu()
        backend.logout_()
        USER_ID = None
        sys.exit()
    elif choice.upper() == 'N':
        display_user_menu()
    else:
        text[0] = "Invalid choice. Please try again!"
        print_box(text)
        choice = input("Enter your choice: ")
    

def main():
    """Main function."""
    database = input("Enter the name of the database: ")
    backend.connect(database)
    display_login_menu()

if __name__ == "__main__":
    main()





