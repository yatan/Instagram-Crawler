import sqlite3

db = sqlite3.connect('./web/data/crawler')
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute('''SELECT nickname FROM users''')
for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
    print('{0}'.format(row['nickname']))
db.close()