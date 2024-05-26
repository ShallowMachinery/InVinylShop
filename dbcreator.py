import mysql.connector as connector
import requests
import datetime

cnx = connector.connect(user="root", password="")
cursor = cnx.cursor()

createdatabase = "CREATE DATABASE InVinylShop"
cursor.execute(createdatabase)

usedatabase = "USE InVinylShop"
cursor.execute(usedatabase)

createAlbumsTable = "CREATE TABLE albums (albumID VARCHAR(255) NOT NULL PRIMARY KEY, albumName VARCHAR(255) NOT NULL, artistName VARCHAR(255) NOT NULL, totalTracks INT(3) NOT NULL, albumGenre VARCHAR(255) NOT NULL, country VARCHAR(255) NOT NULL, albumLength VARCHAR(255) NOT NULL, albumYear YEAR NOT NULL, Price DECIMAL(5,2));"
cursor.execute(createAlbumsTable)

createStocksTable = "CREATE TABLE stocks (albumID VARCHAR(255) NOT NULL PRIMARY KEY, stocksLeft INT NOT NULL, FOREIGN KEY (albumID) REFERENCES albums(albumID));"
cursor.execute(createStocksTable)

createTracksTable = "CREATE TABLE tracks (trackID VARCHAR(255) NOT NULL, trackNumber INT NOT NULL, trackName VARCHAR(255) NOT NULL, artistName VARCHAR(255) NOT NULL, trackLength VARCHAR(10), albumName VARCHAR(255) NOT NULL, albumID VARCHAR(255) NOT NULL, PRIMARY KEY (trackID, albumID), FOREIGN KEY (albumID) REFERENCES albums(albumID));"
cursor.execute(createTracksTable)

createTransactionsTable = "CREATE TABLE transactions (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255) NOT NULL, albumID VARCHAR(255) NOT NULL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);"
cursor.execute(createTransactionsTable)

# Create add album trigger
create_transactions_album_add_trigger_query = """
CREATE TRIGGER transactions_album_add_trigger
AFTER INSERT ON albums
FOR EACH ROW
BEGIN
    DECLARE album_title VARCHAR(255);
    DECLARE artist_name VARCHAR(255);
    SET album_title = (SELECT albumName FROM albums WHERE albumID = NEW.albumID);
    SET artist_name = (SELECT artistName FROM albums WHERE albumID = NEW.albumID);
    INSERT INTO transactions (message, albumID)
    VALUES (CONCAT('"', album_title, '" by ', artist_name, ' was added to the database'), NEW.albumID);
END
"""
cursor.execute(create_transactions_album_add_trigger_query)

# Create delete album trigger
create_transactions_album_delete_trigger_query = """
CREATE TRIGGER transactions_album_delete_trigger
AFTER DELETE ON albums
FOR EACH ROW
BEGIN
    DECLARE album_title VARCHAR(255);
    DECLARE artist_name VARCHAR(255);
    SET album_title = OLD.albumName;
    SET artist_name = OLD.artistName;
    INSERT INTO transactions (message, albumID)
    VALUES (CONCAT('"', album_title, '" by ', artist_name, ' was deleted from the database'), OLD.albumID);
END
"""
cursor.execute(create_transactions_album_delete_trigger_query)

# Create buy album trigger
create_transactions_album_buy_trigger_query = """
CREATE TRIGGER transactions_album_buy_trigger
AFTER UPDATE ON stocks
FOR EACH ROW
BEGIN
    IF NEW.stocksLeft < OLD.stocksLeft THEN
        INSERT INTO transactions (message, albumID)
        VALUES (
            CONCAT('Bought "', (SELECT albumName FROM albums WHERE albumID = NEW.albumID), '" by ',
            (SELECT artistName FROM albums WHERE albumID = NEW.albumID), ', x', OLD.stocksLeft - NEW.stocksLeft),
            NEW.albumID
        );
    END IF;
END;
"""
cursor.execute(create_transactions_album_buy_trigger_query)

# Create update stocks trigger
create_transactions_album_update_stocks_trigger_query = """
CREATE TRIGGER transactions_album_update_stocks_trigger
AFTER UPDATE ON stocks
FOR EACH ROW
BEGIN
    IF NEW.stocksLeft > OLD.stocksLeft THEN
        INSERT INTO transactions (message, albumID)
        VALUES (
            CONCAT('Added x', NEW.stocksLeft - OLD.stocksLeft, ' stocks for "', (SELECT albumName FROM albums WHERE albumID = NEW.albumID), '" by ',
            (SELECT artistName FROM albums WHERE albumID = NEW.albumID)), NEW.albumID
        );
    END IF;
END;
"""
cursor.execute(create_transactions_album_update_stocks_trigger_query)

cnx.commit()