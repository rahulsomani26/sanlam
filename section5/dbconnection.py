from user import User
import sqlite3

# connect to a database
con = sqlite3.connect('registereduser.db')
cur = con.cursor()
# create a table

users = [

    (1, 'rahul', 'rahul@123'),
    (2, 'ujjwal', 'ujjwal@123')
]

cur.execute(
    'create table if not exists USERS(id INTEGER PRIMARY KEY AUTOINCREMENT ,username text,password text)')


try:
    # cur.execute('insert into USERS values(?,?,?)', (1, 'ujjwal', 'kumar'))
    cur.executemany("insert into USERS values(null,?,?)", users)
except Exception as a:
    print(' error {}'.format(a))

result = cur.execute('select * from USERS')
rset = result.fetchall()
print(rset)
con.commit()
con.close()
