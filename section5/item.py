
from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
import sqlite3

# books = [
#     {
#         'ISBN': '978-354-216',
#         'author': 'Jon Mac',
#         'name': 'The man',
#         'quantity': 20
#     },
#     {
#         'ISBN': '128-689-341',
#         'author': 'Michael Jack',
#         'name': 'Although what',
#         'quantity': 10
#     }
# ]


con = sqlite3.connect('books.db')
cur = con.cursor()
cur.execute(
    ' create table if not exists BOOKS(ISBN TEXT PRIMARY KEY,AUTHOR TEXT,NAME TEXT,QUANTITY INTEGER)')
# cur.execute('insert into BOOKS values(?,?,?,?)',
# ('978-354-245', 'MChil', 'one', 10))
con.commit()
con.close()


class Book(Resource):
    # get book by ISBN
    @jwt_required()
    def get(self, ISBN):
        # search for the book with the ISBN , return it otherwise return a message
        # connect to the database
        con = sqlite3.connect('books.db')
        cur = con.cursor()

        sql_query = "select * from BOOKS where ISBN=?"
        result = cur.execute(sql_query, (ISBN,))
        row = result.fetchone()
        con.close()

        if row is not None:
            return {"Book": row}
        return "book not found"

    # create book
    def post(self):

        # collect data
        payload = request.get_json()
        isbn = payload["ISBN"]
        author = payload["author"]
        name = payload["name"]
        quantity = payload["quantity"]
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        result = cur.execute(
            ' select quantity from BOOKS where ISBN=?', (isbn,))
        row = result.fetchone()
        if row is not None:

            cur.execute('update BOOKS set quantity=? where ISBN=?',
                        (row[0] + 1, isbn))
            con.commit()
            con.close()
            return "book with ISBN {}number updated".format(isbn)
        # else create a new book

        con = sqlite3.connect('books.db')
        cur = con.cursor()
        cur.execute('insert into BOOKS values(?,?,?,?)',
                    (isbn, author, name, quantity,))
        con.commit()
        con.close()
        return " Book created ", 201

    def delete(self, ISBN):
        con = sqlite3.connect('books.db')
        cur = con.cursor()

        sql_query = "select * from BOOKS where ISBN=?"
        result = cur.execute(sql_query, (ISBN,))
        row = result.fetchone()

        if row is not None:
            # The book has been found
            # Fire an sql query to delete books
            cur.execute('delete from BOOKS where ISBN=?', (ISBN,))
            con.commit()
            con.close()
            return "Book deleted"
        return "book not found", 404

    # def put(self, ISBN):
    #     pos = 0
    #     for book in books:
    #         if book["ISBN"] == ISBN:
    #             # The book is already there, so update the quantity
    #             book["quantity"] = book["quantity"] + 1
    #             books[pos] = book
    #             return "Book quantity updated by 1"
    #         pos = pos+1

    #     # add the book if it is not in the books list
    #     payload = request.get_json()
    #     isbn = payload["ISBN"]
    #     author = payload["author"]
    #     name = payload["name"]
    #     quantity = payload["quantity"]
    #     newbook = {
    #         "ISBN": isbn,
    #         "author": author,
    #         "name": name,
    #         "quantity": quantity
    #     }

    #     # add this payload to books
    #     books.append(newbook)
    #     return newbook, 201


# Resource for getting all books from the db


class BookList(Resource):
    # returns all the books in the store
    def get(self):
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        sql_query = "select * from BOOKS"
        result = cur.execute(sql_query)
        row = result.fetchall()
        return row
