import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "IsThatRoot?0330",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password is invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)

cursor = db.cursor()
cursor.execute(“SELECT studio, genre FROM movies”)
cursor.execute(“SELECT films FROM movies WHERE run_time < 120”)
cursor.execute(“SELECT director, films FROM movies GROUP BY directors”)
films = cursor.fetchall()
for films in movies:
print(“Movie: {}\n Director:{}\n”.format(director[0], director[1], director[2]))

finally:
    db.close()