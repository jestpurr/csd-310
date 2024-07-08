import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "IsThatRoot?0330",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}


db = mysql.connector.connect(**config)
cursor = db.cursor()
cursor.execute("SELECT * FROM studio")
studios = cursor.fetchall()
print("DISPLAYING STUDIOS")
for studio in studios:
    print(f"Studio ID: {studio[0]}")
    print(f"Studio Name is: {studio[1]}")

cursor.execute("SELECT * FROM genre")
print("DISPLAYING GENRES")
genres = cursor.fetchall()
for genre in genres:
    print(f"Studio ID: {genre[0]}")
    print(f"Genre Name is: {genre[1]}")

cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
print("DISPLAYING MOVIES UNDER 2 HOURS")
twohour = cursor.fetchall()
for movie in twohour:
    print(f"Studio ID: {movie[1]}")
    print(f"Movie Name is: {movie[0]}")

cursor.execute("SELECT film_name, film_director FROM film GROUP BY film_name, film_director ORDER BY film_director")
director_data = cursor.fetchall()
print("DISPLAYING DIRECTORS")
for film in director_data:
    print(f"Studio ID: {film[0]}")
    print(f"Director Name is: {film[1]}")


db.close()