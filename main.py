import admin
import mysql.connector as connector
import collection
import sys

def menu():
    result = True
    print("""+------------------------------------------------------------+
| Hello, user!                                               |
| What would you like to do?                                 |
+------------------------------------------------------------+
| 1 - View our collection!                                   |
| 2 - Search from your search query                          |
| 3 - Search for artist or band                              |
| 4 - Search for genre                                       |
| 5 - Search for the country of release                      |
| 6 - Search for the year of release                         |
| 0 - Exit the program                                       |
+------------------------------------------------------------+""")

    user_input = input("Enter your response: ")
    if not user_input.isdigit():
        print("""
------------------------------------------------------
| ERROR: You didn't enter a value. Please try again. |
------------------------------------------------------
        """)
        return menu()
    user_input = int(user_input)
    if user_input == 1:
        result = collection.view_collection()
    elif user_input == 2:
        query_input = input("Search collection: ")
        result = collection.view_collection_by_query(search=query_input)
    elif user_input == 3:
        artist_name_input = input("Search artist/band: ")
        result = collection.view_collection_by_artist(artist_name_input)
    elif user_input == 4:
        genre_input = input("Search genre: ")
        result = collection.view_collection_by_genre(genre_input)
    elif user_input == 5:
        country_input = input("Search country: ")
        result = collection.view_collection_by_country(country_input)
    elif user_input == 6:
        year_input = input("Search release year: ")
        if not year_input.isdigit():
            print("""
------------------------------------------------------
| ERROR: Invalid year input.                         |
------------------------------------------------------
            """)
            menu()
        result = collection.view_collection_by_year(year_input)
    elif user_input == 177013:
        result = admin.admin_menu()
    elif user_input == 0:
        print("""
+-----------------------------------------+
| Thank you! Exiting the program...       |
+-----------------------------------------+
        """)
        sys.exit()
    else:
        print("""
----------------------------------------------------------
| ERROR: You entered an invalid input. Please try again. |
----------------------------------------------------------
        """)
        return menu()
    
    if result is None:
        menu()

def welcome_art():
    welcome_ascii="""
______________________________________________________________
|   _____            _             _   __ _                  |
|   \_   \_ __/\   /(_)_ __  _   _| | / _\ |__   ___  _ __   |
|    / /\/ '_ \ \ / / | '_ \| | | | | \ \| '_ \ / _ \| '_ \  |
| /\/ /_ | | | \ V /| | | | | |_| | | _\ \ | | | (_) | |_) | |
| \____/ |_| |_|\_/ |_|_| |_|\__, |_| \__/_| |_|\___/| .__/  |
|                            |___/                   |_|     |
|___________________________________________________________ |"""
    print(welcome_ascii)
    print("""+------------------------------------------------------------+
|                  WELCOME TO InVinylShop!                   |
|   The vinyl to CD shop that will relive your nostalgia!    |
+------------------------------------------------------------+""")
    menu()

welcome_art()