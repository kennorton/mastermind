
"""
Project III: An implementation of the Mastermind game

File Name: mastermind
Name:      Kenneth Norton
Course:    CPTR 141
Code Review: 
"""

''' IMPORTED MODULES '''
import os
import sys
import random
from termcolor import colored, cprint

''' STORAGE LISTS AND DICTIONARIES '''
# Storage for master code.
master_code = [] 
# Storage for user guesses and their associated pegs.
user_code_history = []
keypegs = []
# Storage for game settings
settings_data = {
    'game length' : 10,
    'code length' : 4,
    'debug' : 'off'
}

''' GENERAL FUNCTIONS '''
def error_msg():
    ''' Print an error message.'''

    cprint(f"\nBEEP! That's not a valid option... Try again. BOOP!", 'red', attrs=['bold'])

def gen_code():
    ''' Generate a master code with the desired length stored in settings_data['code length']. '''
    intcode = []
    # Create random number and append to temp.
    for i in range(settings_data['code length']):
        intcode.append(random.randint(0,5))
    for i in intcode:
        master_code.append(str(i))

def clear():
    ''' Clear the console. '''

    command = 'clear'
    # If computer is running windows, use cls
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

''' MASTERMIND GAME '''
def game():
    ''' Generate a random code and run the mastermind game. '''

    gen_code()
    get_code()

def game_visual(attempts, error, valid_entries):
    ''' Display a graphic, number of attempts, guess history, and any error messages. '''
    
    clear()
    cprint("+------------------------=[ Valid Numbers ]=------------------------+", 'green', attrs=['bold'])
    valid_numbers()
    cprint("+-------------------------------------------------------------------+", 'green', attrs=['bold'])
    cprint("|                                                                   |", 'green', attrs=['bold'])
    cprint("|                  Enter your code like this: 1010                  |", 'green', attrs=['bold'])
    cprint("|                type 'quit' to go to the main menu.                |", 'green', attrs=['bold'])
    cprint("|                                                                   |", 'green', attrs=['bold'])
    cprint("+-------------------------------------------------------------------+", 'green', attrs=['bold'])
    # Show master code if debug is on.
    if settings_data['debug'] == 'on':
        print(master_code)

    # Show a guess history if user has already guessed.
    if attempts > 0:
        guess_history(attempts)
    # Print an error message if the user has thrown an error.
    if error:
        error_msg()
        error = False

def get_code():
    ''' Get the user to guess the secret code. '''

    error = False
    valid_entries = False
    attempts = 0
    # Get a code from the user until they run out of attempts.
    while attempts < settings_data['game length']:
        print(master_code) # DEBUG
        # Display current game information and menu.
        game_visual(attempts, error, valid_entries)
        if error:
            error = False
        guess = input(colored("\nEnter your code: ", 'cyan', attrs=['bold']))
        # Check to see if guess is the right length and made of numbers that are valid.
        if (len(guess) == settings_data['code length']) and guess.isnumeric():
            # Check to see if guess is made of valid numbers
            valid_entries = True
            attempts += 1
            user_code_history.clear()
            user_code_history.append(str(guess))
            pegcheck(guess)
        # Confirm the user wants to quit if they enter 'quit'.
        elif guess == 'quit':
            quit_check()
        # Throw an error if user enters an option that isn't in the menu.
        else:
            error = True
        # Check to see if user has won.
        if wincheck(keypegs):
            win()
            break      

def valid_numbers():
    ''' Print all valid numbers. '''

    cprint(f"0 1 2 3 4 5", 'yellow', attrs=['bold'] )

def pegcheck(guess):
    ''' Check guess and return cooresponding 'key pegs. '''

    m = master_code.copy()
    u = []
    # Append user and master code to a temporary list.
    for i in guess:
        u.append(i)
    black_pegcheck(m,u)

def black_pegcheck(m, u):
    ''' Check user guess against master list and give 0. '''

    keypegs.clear()
    # Check each pair of indexes for black pegs.
    index = 0
    while index < len(master_code):
        if u[index] == m[index]:
            u[index] = 'b'
            m[index] = 'b'
            keypegs.append(1)
        index += 1
    # Remove the placeholder pegs on both lists.
    for num in range(u.count('b')):
        u.remove('b')
        m.remove('b')
    # Send modified lists to be checked for white pegs.
    white_pegcheck(m,u)

def white_pegcheck(m,u):
    ''' Check user guess against master list and give 0. '''

    # For each item in user code, look for a duplicate in master code.
    for i in u:
        if i in m:
            m.remove(i)
            keypegs.append(0)

def guess_history(attempts):
    ''' Print the user's past attempts. '''
    
    if attempts == (settings_data['game length'] -1):
        cprint(f"\nTHIS IS YOUR FINAL ATTEMPT!", "red", attrs=['bold'])
    else:
        cprint(f"\nYou have made {attempts} attempts.", "white", attrs=['bold'], end= '  ')
    cprint(f"\nYour previous attempt was:\n", "white", attrs=['bold'])
    print(f"Code: {user_code_history}, Information returned: {keypegs}")

def quit_check():
    ''' If the user enters 'quit' while the game is running, prompt the user for confirmation to quit. '''

    clear()
    cprint("+--------------------------------------------------------------------+", 'white', attrs=['bold'])
    cprint("|                                                                    |", 'white', attrs=['bold'])
    cprint("|   Are you sure you want to quit? Any progress will not be saved.   |", 'white', attrs=['bold'])
    cprint("|                                                                    |", 'white', attrs=['bold'])
    cprint("+--------------------------------------------------------------------+", 'white', attrs=['bold'])
    check = input(colored("\nType 'quit' again to exit the game. If you want to continue, type anything else: ", 'cyan', attrs=['bold'])).lower()
    # If user enters 'yes', quit the game.
    if check == 'quit':
        quit()
    # If the user enters anything else, continue the game.
    else:
        pass

def wincheck(keypegs):
    ''' Check to see if user has cracked the code. '''

    # If there are as many black pegs as there are numbers in the code, user has won.
    if keypegs.count(1) == settings_data['code length']:
        return True
    else:
        return False
    
def win():
    ''' Print the win screen. '''

    clear()
    cprint("+-------------------------------------------------------------------+", 'green', attrs=['bold'])
    cprint("|                                                                   |", 'green', attrs=['bold'])
    cprint("|                      YOU CRACKED THE CODE!!!                      |", 'green', attrs=['bold'])
    cprint("|                            CONGRATS!!!                            |", 'green', attrs=['bold'])
    cprint("|                                                                   |", 'green', attrs=['bold'])
    cprint("+-------------------------------------------------------------------+", 'green', attrs=['bold'])

''' MAIN MENU '''
def main_menu():
    ''' Display the main menu and prompt for user navigation. '''

    nav_main = True
    error = False
    while nav_main:
        clear()
        main_menu_visual()
        # Print an error message if the user has thrown an error.
        if error:
            error_msg()
            error = False
        choice = input(colored("\nEnter an option from the menu: ", 'yellow', attrs=['bold'])).lower()
        # Start the game is user enters 'start'.
        if choice == "initiate":
            nav_main = False
            how_to_play()
        # Open the settings menu is user enters 'settings'.
        elif choice == "settings":
            settings_menu()
        # Confirm the user wants to quit if they enter 'quit'.
        elif choice == "quit":
            quit_check()
        # Throw an error if user enters an option that isn't in the menu.
        else:
            error = True

def main_menu_visual():
    ''' Print the visual for the main menu. '''

    cprint("+----------------------=[ CODE CRACKER ]=----------------------+", 'green', attrs=['bold'])
    cprint("|                                                              |", 'green', attrs=['bold'])
    cprint("|                          'Initiate'                          |", 'green', attrs=['bold'])
    cprint("|                          'Settings'                          |", 'green', attrs=['bold'])
    cprint("|                            'Quit'                            |", 'green', attrs=['bold'])
    cprint("|                                                              |", 'green', attrs=['bold'])
    cprint("+--------------------------------------------------------------+", 'green', attrs=['bold'])

''' HOW TO PLAY '''
def how_to_play():
    ''' Display the how-to-play menu and prompt for user navigation. '''

    setup_nav = True
    error = False
    while setup_nav:
        clear()
        how_to_play_visual()
        # If the user enters an invalid entry, print an error.
        if error:
            error_msg()
        choice = input(colored("\nType 'initiate' to begin or 'back' to return to the main menu: ", 'yellow', attrs=['bold']))
        # Begin the game if user enters 'start'.
        if choice == 'initiate':
            setup_nav = False
            game()
        # Navigate to previous menu if user enters 'back'.
        elif choice == 'back':
            setup_nav = False
            main_menu()
        # Throw an error if user enters an option that isn't in the menu.
        else:
            error = True

def how_to_play_visual():
    ''' Print the instructions for Mastermind. '''

    cprint("---------------------------------[ OBJECTIVE BRIEFING ]---------------------------------", 'green', attrs=['bold'])
    cprint(f"\nThe current objective is to correctly guess the password of a computer owned\nby criminal organization and destroy their data!", 'green' )
    cprint(f"\nThe password is {settings_data['code length']} characters long and is made of these numbers:\n", 'green' )
    valid_numbers()
    cprint(f"\nYou must correctly guess each number and its position.", 'green' )
    cprint(f"\nOnce you enter {settings_data['code length']} numbers, I'll attempt a remote breach from this computer!", 'green' )
    cprint(f"The computer on the other end returns some useful information after a breaching attempt:", 'green' )
    cprint(f"\n0 : Means a number is CORRECT but in the INCORRECT position. ", 'yellow' )
    cprint(f"1 : Means a number is CORRECT and in the CORRECT position. Good job!", 'yellow' )

    cprint(f"\nCAREFUL! We only get {settings_data['game length']} attempts to breach the system before someone notices! BEEP BOOP!", 'green' )

''' SETTINGS MENU '''
def settings_menu():
    ''' Display the settings menu and prompt for user navigation. '''

    nav_settings = True
    error = False
    while nav_settings:
        clear()
        settings_menu_visual()
        # Print an error message if the user has thrown an error.
        if error:
            error_msg()
        choice = input(colored("\nEnter an option from the menu: ", 'yellow', attrs=['bold'])).lower()
        # Modify the game length or code length, depending on what is entered.
        if choice == 'code length' or choice == 'game length':
            change_setting(choice)
        # Return to the Main Menu if 'back' is entered as choice.
        elif choice == "debug":
            if settings_data['debug'] == 'on':
                settings_data['debug'] = 'off'
            else:
                settings_data['debug'] = 'on'
        elif choice == "back":
            nav_settings = False
        # Throw an error if user enters an option that isn't in the menu.
        else:
            error = True

def settings_menu_visual():
    ''' Print the visual for the main menu. '''

    cprint("+-------------------------=[ Settings ]=-----------------------+", 'green', attrs=['bold'])
    cprint("|                                                              |", 'green', attrs=['bold'])
    cprint("|                         'game length'                        |", 'green', attrs=['bold'])
    cprint("|                         'code length'                        |", 'green', attrs=['bold'])
    cprint("|                         'debug' mode                         |", 'green', attrs=['bold'])
    cprint("|                                                              |", 'green', attrs=['bold'])
    cprint("|                            'Back'                            |", 'green', attrs=['bold'])
    cprint("|                                                              |", 'green', attrs=['bold'])
    cprint("+--------------------------------------------------------------+", 'green', attrs=['bold'])   
    if settings_data['debug'] == 'on':
        print("debug is on.")
    if settings_data['debug'] == 'off':
        print("debug is off.")

''' MODIFIABLE SETTINGS '''
def change_setting(choice):
    ''' Modify the setting selected in the settings menu. The two modifiable settings are 'game length' and 'code length'. '''

    sub_menu = True
    error = False
    while sub_menu:
        clear()
        settings_menu_visual()
        # Print an error message if the user has thrown an error.
        if error:
            error_msg()
        # Print a message telling the user what setting they are modifying, as well as its current value.
        cprint(f"\nThe current {choice} is {settings_data[choice]}.", "white", attrs=['bold'])
        modify_option = input(colored(f"\nEnter a custom {choice} or leave blank to keep current length. Type 'default' to return to default setting: ", "cyan", attrs=['bold']))
        if len(modify_option) > 0:
            # Save the user's input if it is a valid integer.
            if modify_option.isdigit():
                settings_data[choice] = int(modify_option)
                sub_menu = False
            # Reset the option to 'default' (game length: 10, code length: 4).
            elif modify_option == 'default':
                if choice == 'game length':
                    settings_data[choice] = 10
                elif choice == 'code length':
                    settings_data[choice] = 4
                sub_menu = False
            # Throw an error if input is not a number, 'default', or left blank.
            else:
                error = True
        # Keep the current setting if nothing is input.      
        else:
            sub_menu = False

#MAIN CODE BODY
main_menu()