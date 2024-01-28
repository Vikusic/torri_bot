import psycopg2

conn = psycopg2.connect(dbname = 'metanit', user = 'postgres', password = 'root', host = 'localhost')
cursor = conn.cursor()

# people = [('Sam', 44), ("Alise", 33), ("Kate", 25)]
# cursor.executemany("INSERT INTO people (name, age) VALUES (%s, %s)", people)
# conn.commit()
# print(':)')

# cursor.execute("SELECT * FROM people")
# print(cursor.fetchone())

# cursor.execute("UPDATE people SET name = %s WHERE name = %s", ("Tomas", "Tom"))
cursor.execute("UPDATE people SET name = 'Tomas' WHERE name = 'Tom'")
conn.commit()

cursor.close()
conn.close()