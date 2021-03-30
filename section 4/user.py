import sqlite3
from flask_restful import Resource, reqparse
from flask import Flask, request


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def get_user_by_name(cls, username):
        # create a connection
        con = sqlite3.connect('registereduser.db')
        # create a cursor object
        cur = con.cursor()

        # Fire sql query to insert values in the database
        result = cur.execute(
            'select * from USERS where username=?', (username,))
        row = result.fetchone()
        if row is not None:
            user = cls(row[0], row[1], row[2])
            print(row[0])
        else:
            user = None
        return user

    @classmethod
    def get_user_by_id(cls, _id):
        # create a connection
        con = sqlite3.connect('registereduser.db')
        # create a cursor object
        cur = con.cursor()

        # Fire sql query to insert values in the database
        result = cur.execute(
            'select * from USERS where id=?', (_id,))
        row = result.fetchone()
        if row is not None:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        return user


class RegisterdUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help='Username required')
    parser.add_argument('password', type=str, required=True,
                        help='Password required')

    def post(self):
        # payload = request.get_json()  try using this aswell and see whether it works or not
        # add some code here

        payload = RegisterdUser.parser.parse_args()
        if User.get_user_by_name(payload['username']):
            return{"user already exists ": payload['username']}, 400

        con = sqlite3.connect('registereduser.db')
        cur = con.cursor()
        cur.execute('insert into USERS values(null,?,?)',
                    (payload["username"], payload["password"]))
        con.commit()
        con.close()
        return "user created", 201
