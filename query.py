import mysql.connector as connector
import pandas as pd
import decimal
import admin

cnx = connector.connect(user="root", password="", database = "InVinylShop")
cursor = cnx.cursor()

CURRENCYPHPUSD = decimal.Decimal(55.64)
QUERY_ALL = "SELECT '', albums.albumID, albums.albumName, albums.artistName, albums.albumYear, albums.albumGenre, albums.totalTracks, albums.country, albums.price, stocks.stocksLeft FROM InVinylShop.albums JOIN InVinylShop.stocks ON albums.albumID = stocks.albumID"
QUERY_ORDER = "ORDER BY artistName ASC, albumYear ASC, albumName ASC"

def query_all_collection():
    cursor.execute(QUERY_ALL)
    album_entries = cursor.fetchall()
    album_entries = [(i+1,) + tuple(item[1:]) for i, item in enumerate(album_entries)]
    return album_entries

def query_collection(search):
    query = f"{QUERY_ALL} WHERE albumName like '%{search}%' OR artistName like '%{search}%' {QUERY_ORDER}"
    cursor.execute(query)
    album_entries = cursor.fetchall()
    album_entries = [(i+1,) + tuple(item[1:]) for i, item in enumerate(album_entries)]
    return album_entries

def query_collection_by_artist(artist_search):
    query = f"{QUERY_ALL} WHERE artistName like '%{artist_search}%' {QUERY_ORDER}"
    cursor.execute(query)
    album_entries = cursor.fetchall()
    album_entries = [(i+1,) + tuple(item[1:]) for i, item in enumerate(album_entries)]
    return album_entries

def query_collection_by_genre(genre_search):
    query = f"{QUERY_ALL} WHERE albumGenre like '%{genre_search}%' {QUERY_ORDER}"
    cursor.execute(query)
    album_entries = cursor.fetchall()
    album_entries = [(i+1,) + tuple(item[1:]) for i, item in enumerate(album_entries)]
    return album_entries

def query_collection_by_country(country_search):
    query = f"{QUERY_ALL} WHERE country like '%{country_search}%' {QUERY_ORDER}"
    cursor.execute(query)
    album_entries = cursor.fetchall()
    album_entries = [(i+1,) + tuple(item[1:]) for i, item in enumerate(album_entries)]
    return album_entries

def query_collection_by_year(year_search):
    query = f"{QUERY_ALL} WHERE albumYear like '%{year_search}%' {QUERY_ORDER}"
    cursor.execute(query)
    album_entries = cursor.fetchall()
    album_entries = [(i+1,) + tuple(item[1:]) for i, item in enumerate(album_entries)]
    return album_entries

def query_stocks(album_id):
    query = f"SELECT stocksLeft FROM InVinylShop.stocks WHERE albumID = '{album_id}'"
    cursor.execute(query)
    stock_count = cursor.fetchone()
    return stock_count[0]

def query_album_details(artist_name, album_id):
    query = f"SELECT trackNumber, trackName, trackLength FROM InVinylShop.tracks WHERE artistName = '{artist_name}' AND albumID = '{album_id}' ORDER BY trackNumber ASC"
    cursor.execute(query)
    album_details = cursor.fetchall()
    return album_details

def query_transactions():
    cursor.execute("SELECT message, date FROM InVinylShop.transactions")
    transaction_entries = cursor.fetchall()
    return transaction_entries

def update_stocks(album_id, stock_count):
    query = f"UPDATE InVinylShop.stocks SET stocksLeft = {stock_count} WHERE albumID = '{album_id}'"
    cursor.execute(query)
    cnx.commit()

def add_album(album_id, album_name, artist_name, total_tracks, album_genre, country, album_length, album_year, price):
    query = "INSERT INTO albums (albumID, albumName, artistName, totalTracks, albumGenre, country, albumLength, albumYear, Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    album_values = (album_id, album_name, artist_name, total_tracks, album_genre, country, album_length, album_year, price)
    cursor.execute(query, album_values)
    cnx.commit()

def delete_album(album_id):
    query = f"DELETE FROM InVinylShop.albums WHERE albumID = '{album_id}'"
    cursor.execute(query)
    cnx.commit()

def add_album_tracks(track_values):
    query = "INSERT INTO tracks (trackID, trackNumber, trackName, artistName, tracklength, albumName, albumID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, track_values)
    cnx.commit()

def add_album_stocks(album_id):
    query = "INSERT INTO stocks (albumID, stocksLeft) VALUES (%s, %s)"
    stock_values = (album_id, 5)
    cursor.execute(query, stock_values)
    cnx.commit()

def delete_album_stocks(album_id):
    query = f"DELETE FROM InVinylShop.stocks WHERE albumID = '{album_id}'"
    cursor.execute(query)
    cnx.commit()

def delete_album_tracks(album_name, artist_name):
    query = f"DELETE FROM InVinylShop.tracks WHERE albumName = '{album_name}' AND artistName = '{artist_name}'"
    cursor.execute(query)
    cnx.commit()

def backup_album_links():
    query = "SELECT CONCAT('https://musicbrainz.org/release/', albumID, ' - ', country) AS release_links FROM albums GROUP BY albumName, artistName;"
    cursor.execute(query)
    results = cursor.fetchall()
    output_file = "backup album release links.txt"
    with open(output_file, "w") as file:
        for row in results:
            concatenated_id_and_country = row[0]
            file.write(concatenated_id_and_country + "\n\n")
            print("""+----------------------------------------------------+
| INFORMATION: Albums backed up succesfully!         |
+----------------------------------------------------+
                    """)
    