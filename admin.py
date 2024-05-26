import mysql.connector as connector
import requests
import datetime
import re
import query
import collection

cnx = connector.connect(user="root", password="", database = "InVinylShop")
cursor = cnx.cursor()

def milliseconds_to_mmss(milliseconds):
    delta = datetime.timedelta(milliseconds=milliseconds)
    minutes = delta.total_seconds() // 60
    seconds = delta.total_seconds() % 60
    mmss_format = f"{int(minutes):02d}:{int(seconds):02d}"
    return mmss_format

def get_album_tracks(mbid, country):
    # MusicBrainz API endpoint for the release group
    url = f"https://musicbrainz.org/ws/2/release/{mbid}?inc=recordings+artists+genres&fmt=json"

    # Send GET request to the MusicBrainz API
    response = requests.get(url, headers={"Accept": "application/json"})
    if response.status_code != 200:
        print("""----------------------------------------------------------
| ERROR: The link you entered is not valid or not found. |
----------------------------------------------------------""")
        return None
    response = response.json()

    # albums
    album_id = response["id"]
    album_name = response["title"]
    artist_name = response["artist-credit"][0]["name"]
    total_tracks = response["media"][0]["track-count"]
    try:
        album_genre = response["genres"][0]["name"]
    except IndexError:
        try:
            album_genre = response["artist-credit"][0]["artist"]["genres"][0]["name"]
        except IndexError:
            album_genre = ""
    album_year = response["release-events"][0]["date"]
    album_year = album_year[:4]

    album_length = 0
    try:
        for track in response["media"][0]["tracks"]:
            album_length = album_length + track["length"]
    except:
        print("""----------------------------------------------------------
| ERROR: The track lengths are invalid for this release. |
| Please send another release link.                      |
----------------------------------------------------------""")
        return "add_album"
    
    album_length = milliseconds_to_mmss(album_length)

    price_ug = 10.99
    price_ph = 5.99
    price_xw = 8.99

    if country == "ph":
        price = price_ph + total_tracks
    elif country == "ug":
        price = price_ug + total_tracks
    elif country == "xw":
        price = price_xw + total_tracks
    else:
        print("""---------------------------
| ERROR: Invalid country. |
---------------------------""")
        return None

    # tracks

    track_values = []

    artist_name = response["artist-credit"][0]["name"]
    album_name = response["title"]

    for track in response["media"][0]["tracks"]:
        track_length = track["length"]
        track_length = milliseconds_to_mmss(track_length)
        track_id = track["id"]
        track_number = track["position"]
        track_title = track["title"]
        track_data = (track_id, track_number, track_title, artist_name, track_length, album_name, album_id)
        track_values.append(track_data)

    try:
        query.add_album(album_id, album_name, artist_name, total_tracks, album_genre, country, album_length, album_year, price)
    except connector.errors.IntegrityError as error:
        if error.errno == connector.errorcode.ER_DUP_ENTRY:
            print("""------------------------------------------------------------
| ERROR: This release is already imported to the database. |
| Please send another release link.                        |
------------------------------------------------------------""")
        else:
            print("\nAn error occurred:", error)
        return "add_album"

    try:
        query.add_album_stocks(album_id)
    except connector.errors.IntegrityError as error:
        if error.errno == connector.errorcode.ER_DUP_ENTRY:
            print("""------------------------------------------------------------
| ERROR: This release is already imported to the database. |
| Please send another release link.                        |
------------------------------------------------------------""")
        else:
            print("\nAn error occurred:", error)

    try:
        query.add_album_tracks(track_values)
    except connector.errors.IntegrityError as error:
        if error.errno == connector.errorcode.ER_DUP_ENTRY:
            print("""------------------------------------------------------------
| ERROR: This release is already imported to the database. |
| Please send another release link.                        |
------------------------------------------------------------""")
        else:
            print("An error occurred:", error)

    print(f"""+---------------------------------------------------------------
| INFORMATION: The album \"{album_name}\" by {artist_name}
| was successfully added to the database.
+---------------------------------------------------------------""")

def add_album():
    link_input = input("\nMusicBrainz link: ")
    country_input = input("Album country origin: ")
    link_pattern = r"https?://musicbrainz.org/release/[a-fA-F0-9-]+"
    matches = re.findall(link_pattern, link_input)
    
    if country_input is None:
        print("""
--------------------------------
| ERROR: Input doesn't exists. |
--------------------------------
        """)
        return add_album()
    if country_input.lower() not in ['ph', 'ug', 'xw']:
        print("""
---------------------------
| ERROR: Invalid country. |
---------------------------
        """)
        return add_album()
    
    if matches:
        for link in matches:
            release_id = link.split("/release/")[1]
    else:
        print("""
----------------------------------------------------------
| ERROR: The link you entered is not valid or not found. |
----------------------------------------------------------
        """)
        return add_album()
    
    result = get_album_tracks(release_id, country_input)
    if result == "add_album":
        return add_album()
    
    return admin_menu()
    
def delete_album():
    result = query.query_all_collection()
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Price in USD', 'Stocks']
    collection.display_collection("delete_album", 'All', result, original_columns, column_to_display)
    return admin_menu()

def update_stocks():
    result = query.query_all_collection()
    original_columns = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Year released', 'Album genre', 'Total tracks', 'Country', 'Price in USD', 'Stocks']
    column_to_display = ['Entry no.', 'Album ID', 'Album name', 'Artist name', 'Price in USD', 'Stocks']
    collection.display_collection("update_stocks", 'All', result, original_columns, column_to_display)
    return admin_menu()

def view_transactions():
    collection.view_transactions()
    return admin_menu()

def admin_menu():
    print("""
+------------------------------------------------------------+
| Hello, Administrator!                                      |
| What would you like to do?                                 |
+------------------------------------------------------------+
| 1 - Add album                                              |
| 2 - Delete album                                           |
| 3 - Update album stocks                                    |
| 4 - View transaction history                               |
| 5 - Backup album release links                             |
| 0 - Go back to main menu                                   |
+------------------------------------------------------------+""")

    user_input = input("Enter your response: ")
    if not user_input.isdigit():
        print("""
------------------------------------------------------
| ERROR: You didn't enter a value. Please try again. |
------------------------------------------------------
        """)
        return admin_menu()
    user_input = int(user_input)
    if user_input == 1:
        add_album()
    elif user_input == 2:
        delete_album()
    elif user_input == 3:
        update_stocks()
    elif user_input == 4:
        view_transactions()
    elif user_input == 5:
        query.backup_album_links()
    elif user_input == 0:
        return None
    else:
        print("""
----------------------------------------------------------
| ERROR: You entered an invalid input. Please try again. |
----------------------------------------------------------
        """)
        return admin_menu()