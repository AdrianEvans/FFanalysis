import csv
import MySQLdb

f=open("fossil-finder-classifications-000.csv")

conn = MySQLdb.connect("server-name-here","user-name-here","password-here","database-name-here")
c = conn.cursor()

for row in csv.reader(f):
    c.execute("INSERT INTO raw_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)",(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
    conn.commit()
    print(row[0])
