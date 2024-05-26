import mysql.connector as connector
import decimal
import query

cnx = connector.connect(user="root", password="", database = "InVinylShop")
cursor = cnx.cursor()
currencyPhpUSD = decimal.Decimal(55.64)

def buy(album_entry, stock_count, final_price):
    album_entry_number, album_id, album_name, artist_name, album_year, album_genre, total_tracks, country, price, stocks = album_entry

    quantity = input("\nHow many albums do you want to buy?: ")
    if not quantity.isdigit():
        print("""------------------------------------------------------
| ERROR: You didn't enter a value. Please try again. |
------------------------------------------------------""")
        return buy(album_entry, stock_count, final_price)
    elif int(quantity) > 0:  # Convert quantity to an integer for comparison
        stock_count -= int(quantity)
        cost = float(final_price) * float(quantity)
        query.update_stocks(album_id, stock_count)
        input(f"""+----------------------------------------------------------------------------------------
| INFORMATION: Successfully bought \"{album_name}\" by {artist_name} x{quantity} for Php{cost}.
| Press enter key to go back to menu.
+------------------------------------------------------------------------------------------------""")
        return None
    elif int(quantity) > stock_count:  # Convert quantity to an integer for comparison
        print("""-----------------------------------------------------------------------------------
| ERROR: You have entered a value higher than stocks remaining. Please try again. |
-----------------------------------------------------------------------------------""")
        buy(album_entry, stock_count, final_price)
    else:
        print("""---------------------------------------------------------------------
| ERROR: You have entered an invalid value. Please try again.       |
---------------------------------------------------------------------""")
        buy(album_entry, stock_count, final_price)

def update_stocks(album_entries, entry_number):
    for album_entry in album_entries:
        album_entry_number, album_id, album_name, artist_name, album_year, album_genre, total_tracks, country, price, stocks = album_entry
        if album_entry_number == entry_number:
            final_price = (price * currencyPhpUSD).quantize(decimal.Decimal('0.00'))
            print(f"""+----------------------------------------------
| Album details:                          
+----------------------------------------------
| Album title : {album_name}
| Artist name  : {artist_name}
| Price       : Php{final_price}
| Stocks left : {total_tracks}
+----------------------------------------------
            """)

            choice = input("\nDo you want to add stocks?\nEnter your response (y/n): ")
            if choice.lower() == 'y':
                quantity = input("How many stocks? Enter a value: ")
                if not quantity.isdigit():
                    print("""---------------------------------------------------------------------
| ERROR: You have entered an invalid value. Please try again.       |
---------------------------------------------------------------------""")
                    return update_stocks(album_entries, entry_number)
                else:
                    stocks = stocks + int(quantity)
                    query.update_stocks(album_id, stocks)
                    input(f"""+----------------------------------------------------------------------------------------
| INFORMATION: Successfully updated the stocks of \"{album_name}\" by {artist_name}, adding {quantity} stock/s.
| Press enter key to go back to menu.
+------------------------------------------------------------------------------------------------""")
                    return None
            elif choice.lower() == 'n':
                return None
            else:
                print("""-------------------------------------------------
| ERROR: Invalid input.                         |
-------------------------------------------------""")
                return None