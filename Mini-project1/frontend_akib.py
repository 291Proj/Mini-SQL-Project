import backend
import sys


USER_ID = None



def print_box(text, padding=2):
    '''Formats the box and prints it'''

    max_line_length = max(len(line) for line in text)
    width = max(max_line_length + 2 * padding, 30)
    border = "-" * width

    print("\n " + border)

    for line in text:
        left_padding = " " * padding
        right_padding = " " * (width - len(line) - len(left_padding))
        print("|" + left_padding + line + right_padding + "|")

    print(" " + border + "\n")






def display_login_menu():
    '''Displays Login menu'''

    #Display box
    text = ["Welcome to the Twitter!",
            "1. Press 'L' to Login",
            "2. Press 'S' to Sign Up",
            "3. Press 'Q' to Quit"]
    print_box(text)
    choice = input("Enter your choice: ")

    #Choice loop
    while True:
        if choice.upper() == 'L':
            return login()
        elif choice.upper() == 'S':
            return sign_up()
        elif choice.upper() == 'Q':
            exit_program()
            return
        else:
            text[0] = "Invalid choice. Please try again!"
            print_box(text)
            choice = input("Enter your choice: ")






def login():
    '''Handles user login'''

    global USER_ID

    user_id = input("Enter your User ID: ")
    password = input("Enter your password: ")
    logedin = backend.validate_user_login(user_id, password)

    while True:

        if logedin :
            USER_ID = user_id
            display_user_menu() # successful login takes you to user menu
            break

        else:

            #message for wrong input
            text = ["Invalid User ID or password.",
                    "Please try again."]
            print_box(text)

            user_id = input("Enter your User ID: ")
            password = input("Enter your password: ")
            logedin = backend.validate_user_login(user_id, password)
                



def sign_up():
    '''Handles user signup'''
   
    global USER_ID


    username = input("Enter a new user name: ")

    #Validates all the inputs 
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
        text = ["Invalid timezone.",
                "Timezone must be a number between -12 and 14.",
                "Please try again."]
        print_box(text)
        timezone = input("Enter your timezone: ")


    password = input("Enter a new password: ")

    #All validations done
    user_id = backend.user_signup(password, username, email ,city, timezone)
    text = ["You have successfully signed up!", "Your user ID is: " + str(user_id)]
    USER_ID = user_id
    print_box(text)
    display_user_menu()




def exit_program():
    '''Exits Program'''

    text = ["Are you sure you want to exit?",
            "1. Press Y for Yes",
            "2. Press N for No"]
    print_box(text)

    choice = input("Enter your choice: ")
    if choice.upper() == 'Y':
        text = ["Thank you for using Twitter!",
                "Goodbye!"]
        print_box(text)
        #sys.exit()
    elif choice.upper() == 'N':
        return
    else:
        text[0] = "Invalid choice. Please try again!"
        print_box(text)
        choice = input("Enter your choice: ")




























def display_list():
    '''Displays lists if tweets/users in format'''


def display_feed():
    '''Feed after user logs in'''




# User Interface
def display_user_menu():
    ''' User wishes to use the program's other functionalities'''
        

def search_for_tweets():
    '''Functionality 1'''



def search_for_users():
    '''Functionality 2'''
    


def post_a_tweets():
    '''Functionality 3'''
    
def list_followers():
    '''Functionality 4'''
   

def logout_():
    '''Functionality 5'''
    







   

def main():
    
    backend.connect("test1.db")
    display_login_menu()





if __name__ == "__main__":
    main()