import sqlite3
conn = sqlite3.connect('results.db')
cursor = conn.cursor()
cursor.execute('''SELECT * FROM  urls''')
rows = cursor.fetchall()
c=0
for row in rows:
    print(row)
    c+=1
print(f"{c} internships found")
#cursor.execute("DROP TABLE IF EXISTS urls")
conn.close()
