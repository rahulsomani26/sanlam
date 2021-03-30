from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from secure import authenticate, identity
from user import User, RegisterdUser
from item import Book, BookList


# create app instance

app = Flask(__name__)
# create api instance of app

api = Api(app)
app.secret_key = 'rahul@123'
# will create an endpoint 127.0.0.0:5000/auth
jwt = JWT(app, authenticate, identity)


@app.route('/')
def index():
    return '''
                <html>
                <head>
                <title>
                    Home page</title>
                     <style>
                    
                    body{
                        background:blue;
                        height:100vh;
                    }
                    .wrapper{
                        height:10vh;
                        background:yellow;
                    }
                    
                    
                    </style>
                   
                </head>
                <body>
                    <div class="wrapper">

                    </div
                
                </body>
            '''


# create end points to the resource
api.add_resource(Book, '/book/<ISBN>', '/book')
api.add_resource(BookList, '/books')  # returns all the books from the database
api.add_resource(RegisterdUser, '/register')
# run the app
app.run(debug=True)
