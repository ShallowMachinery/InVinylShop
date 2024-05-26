import mysql.connector as connector
import pandas as pd
import decimal
import transaction
import query

cnx = connector.connect(user="root", password="", database = "InVinylShop")
cursor = cnx.cursor()
currencyPhpUSD = decimal.Decimal(55.64)

def view_album(album_entries, entry_number):
    for album_entry in album_entries:
        album_entry_number, album_id, album_name, artist_name, album_year, album_genre, total_tracks, country, price, stocks = album_entry
        if album_entry_number == entry_number:
            final_price = (price * currencyPhpUSD).quantize(decimal.Decimal('0.00'))
            print(f"""+----------------------------------------------
| Album details:                          
+----------------------------------------------
| Album title   : {album_name}
| Artist name   : {artist_name}
| Year released : {album_year}
| Genre         : {album_genre}
| Country       : {country}
| Price         : Php{final_price}
| No. of tracks : {total_tracks}""")
            album_details = query.query_album_details(artist_name, album_id)
            print(f"""+--------------------------------------------------------
| Tracks from the album {album_name}:                     
+--------------------------------------------------------""")
            for track in album_details:
                track_number, track_name, track_length = track 
                print(f"| {track_number}. {track_name} - {track_length}")
            
            stock_count = query.query_stocks(album_id)
            print(f"""+----------------------------------------------+
| Stocks left: {stock_count}                   """)
            if stock_count == 0:
                print("""+---------------------------------------------+
| INFORMATION: This album is sold out!        |
+---------------------------------------------+""")
                return None
            else:
                choice = input("""+---------------------------------------------+
Do you want to buy this album? (y/n): """)
                if choice.lower() == 'y':
                    result = transaction.buy(album_entry, stock_count, final_price)
                    if result is None:
                        return None
                elif choice.lower() == 'n':
                    return None
                else:
                    print("""-------------------------------------------------
| ERROR: Invalid input.                         |
-------------------------------------------------""")
                    return None
                
def delete_album(album_entries, entry_number):
    for album_entry in album_entries:
        album_entry_number, album_id, album_name, artist_name, album_year, album_genre, total_tracks, country, price, stocks = album_entry
        if album_entry_number == entry_number:
            final_price = (price * currencyPhpUSD).quantize(decimal.Decimal('0.00'))
            print(f"""+----------------------------------------------
| Album details:                          
+----------------------------------------------
| Album title : {album_name}
| Artist name : {artist_name}
| Price       : Php{final_price}
| Stocks left : {stocks}
+----------------------------------------------
            """)

            choice = input("Are you sure you want to delete this album? This action is irreversible.\nEnter your response (y/n): ")
            if choice.lower() == 'y':
                query.delete_album_tracks(album_name, artist_name)
                query.delete_album_stocks(album_id)
                query.delete_album(album_id)
                input("""+-----------------------------------------------------------------------
| Successfully deleted the album \"{album_name}\" by {artist_name}                
| Press enter key to go back to menu.  
+-----------------------------------------------------------------------""")
                return None
            elif choice.lower() == 'n':
                return None
            else:
                print("""-------------------------------------------------
| ERROR: Invalid input.                         |
-------------------------------------------------
                    """)
                return None

def display_collection(admin, search, album_entries, original_columns, column_to_display):
    album_entries_str = str(album_entries)
    if album_entries_str == "[]":
        print("""+-----------------------------------------------+
| INFORMATION: No albums found.                 |
+-----------------------------------------------+
                    """)
        return None

    total_entries = len(album_entries)
    page_size = 10
    current_page = 1

    total_pages = total_entries // page_size
    if total_entries % page_size != 0:
        total_pages += 1

    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        current_page_entries = album_entries[start_index:end_index]
        print(f"""+------------------------------------------------------
| Showing results for: {search}                        
+------------------------------------------------------""")
        df = pd.DataFrame(current_page_entries, columns=original_columns)
        print(df[column_to_display].to_string(index=False))

        print(f"""+------------------------------------------------------+
| Page {current_page}/{total_pages}                    
+------------------------------------------------------+
| What do you want to do next?                         |
| Entry number - select the album associated with it   |
| N - Next page                                        |
| P - Previous page                                    |
| Q - Quit to menu                                     |
+------------------------------------------------------+""")
        choice = input(">>>>>> ").upper()
        if choice is None:
            print("""------------------------------------------------------
| ERROR: You didn't enter a value. Please try again. |
------------------------------------------------------
                    """)
            return None
        if choice.upper() == "N":
        # Go to the next page if available
            if current_page < total_pages:
                current_page += 1
            else:
                current_page = 1  # Loop back to the first page
        elif choice.upper() == "P":
            # Go to the previous page if available
            if current_page > 1:
                current_page -= 1
            else:
                current_page = total_pages  # Loop back to the last page
        elif choice.upper() == "Q":
            # Quit to the menu
            return None

        elif choice.isdigit():
            entry_number = int(choice)
            if admin == "delete_album":
                result = delete_album(album_entries, entry_number)
                album_entries = query.query_all_collection()
                return display_collection(admin, search, album_entries, original_columns, column_to_display)
            elif admin == "update_stocks":
                result = transaction.update_stocks(album_entries, entry_number)
                album_entries = query.query_all_collection()
                return display_collection(admin, search, album_entries, original_columns, column_to_display)
            else:
                result = view_album(album_entries, entry_number)
                return display_collection(admin, search, album_entries, original_columns, column_to_display)
        else:
            print("""------------------------------------------------------
| ERROR: Invalid input.                              |
------------------------------------------------------
                    """)
            return None
        
def view_collection():
    result = query.query_all_collection()
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album name', 'Artist name', 'Year released', 'Price in USD', 'Stocks']
    display_collection(None, 'All', result, original_columns, column_to_display)

def view_collection_by_query(search):
    result = query.query_collection(search)
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album name', 'Artist name', 'Year released', 'Price in USD', 'Stocks']
    display_collection(None, search, result, original_columns, column_to_display)

def view_collection_by_artist(artist_search):
    result = query.query_collection_by_artist(artist_search)
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album name', 'Artist name', 'Year released', 'Price in USD', 'Stocks']
    display_collection(None, artist_search, result, original_columns, column_to_display)

def view_collection_by_genre(genre_search):
    result = query.query_collection_by_genre(genre_search)
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Price in USD', 'Stocks']
    display_collection(None, genre_search, result, original_columns, column_to_display)

def view_collection_by_country(country_search):
    if country_search.lower() in ["philippines, ph"]:
        country_search == "ph"
    elif country_search.lower() in ["united states", "united kingdom", "us", "uk"]:
        country_search == "ug"
    else:
        country_search == "xw"
    result = query.query_collection_by_country(country_search)
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album name', 'Artist name', 'Year released', 'Country', 'Price in USD', 'Stocks']
    display_collection(None, country_search, result, original_columns, column_to_display)

def view_collection_by_year(year_search):
    result = query.query_collection_by_year(year_search)
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album name', 'Artist name', 'Year released', 'Price in USD', 'Stocks']
    display_collection(None, year_search, result, original_columns, column_to_display)

def display_transactions(transaction_entries, original_columns):
    transaction_entries_str = str(transaction_entries)
    if transaction_entries_str == "[]":
        print(f"""+-----------------------------------------------+
| INFORMATION: No albums found.                 |
+-----------------------------------------------+
                    """)
        return None

    total_entries = len(transaction_entries)
    page_size = 10
    current_page = 1

    total_pages = total_entries // page_size
    if total_entries % page_size != 0:
        total_pages += 1

    while True:
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        current_page_entries = transaction_entries[start_index:end_index]
        print(f"""+------------------------------------------------------+
| Transaction history:                                 |
+------------------------------------------------------+""")
        df = pd.DataFrame(current_page_entries, columns=original_columns)
        print(df[original_columns].to_string(index=False))

        print(f"""+------------------------------------------------------+
| Page {current_page}/{total_pages}                    |
+------------------------------------------------------+
| What do you want to do next?                         |
| Entry number - select the album associated with it   |
| N - Next page                                        |
| P - Previous page                                    |
| Q - Quit to menu                                     |
+------------------------------------------------------+""")
        choice = input(">>>>>> ").upper()
        if choice is None:
            print("""------------------------------------------------------
| ERROR: You didn't enter a value. Please try again. |
------------------------------------------------------
                    """)
            return None
        if choice.upper() == "N":
        # Go to the next page if available
            if current_page < total_pages:
                current_page += 1
            else:
                current_page = 1  # Loop back to the first page
        elif choice.upper() == "P":
            # Go to the previous page if available
            if current_page > 1:
                current_page -= 1
            else:
                current_page = total_pages  # Loop back to the last page
        elif choice.upper() == "Q":
            # Quit to the menu
            return None
        else:
            print("""------------------------------------------------------
| ERROR: Invalid input.                              |
------------------------------------------------------
                    """)
            return None

def view_transactions():
    result = query.query_transactions()
    original_columns = ['Message', 'Timestamp',]
    display_transactions(result, original_columns)