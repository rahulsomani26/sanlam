from flask import Flask, request
from flask_restful import Resource, Api

# create app instance
app = Flask(__name__)
# create api instance of app
api = Api(app)

# create in-memory database of books
books = [
    {
        'ISBN': '978-354-216',
        'author': 'Jon Mac',
        'name': 'The man',
        'quantity': 20
    },
    {
        'ISBN': '128-689-341',
        'author': 'Michael Jack',
        'name': 'Although what',
        'quantity': 10
    }
]

# create a Resource Book


class Book(Resource):
    # get book by ISBN
    def get(self, ISBN):
        # search for the book with the ISBN , return it otherwise return a message
        for book in books:
            if book['ISBN'] == ISBN:
                return book
        return " Book Not Found"

    # create book
    def post(self, ISBN):
        # check whether ISBN exists or not
        for book in books:
            if book['ISBN'] == ISBN:
                # add only quantity
                book['quantity'] = book['quantity'] + 1

                # this line will not work the way we expect it to work.
                books.extend(book)
                return book
        # otherwise add the book to the books db

        # collect data
        payload = request.get_json()
        isbn = payload['ISBN']
        author = payload['author']
        name = payload['name']
        quantity = payload['quantity']
        newbook = {
            "ISBN": isbn,
            "author": author,
            "name": name,
            "quantity": quantity
        }

        # add this payload to books
        books.append(newbook)
        return newbook

# Resource for getting all books from the db


class BookList(Resource):
    def get(self):
        return books


# create end points to the resource
api.add_resource(Book, '/book/<ISBN>')
api.add_resource(BookList, '/books')  # returns all the books
# run the app
app.run(debug=True)
