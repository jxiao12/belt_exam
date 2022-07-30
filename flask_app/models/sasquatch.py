from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users

class Sasquatch:
    db_name = "SasquatchWebsighting"

    def __init__(self, data):
        self.id = data["id"]
        self.location = data["location"]
        self.happend = data["happend"]
        self.count = data["count"]
        self.date = data["date"]
        self.create_at = data['create_at']
        self.upload_at = data['upload_at']
        self.users_id = data['users_id']
        self.creator = None


    @classmethod
    def save(cls, data):
        query = "INSERT INTO sasquatch (location, happend, count, date, users_id) VALUES(%(location)s,%(happend)s, %(count)s, %(date)s, %(users_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sasquatch;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_recipes = []
        for row in results:
            author = ""
            querys = "SELECT * FROM users;"
            res = connectToMySQL(cls.db_name).query_db(querys)
            for result in res:
                creator_info = {}
                if row["users_id"] == result["id"]:
                    author = result["first_name"] + " " + result["last_name"]
            all_recipes.append( [author, cls(row)] )
        print(all_recipes[0][0])
        return all_recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sasquatch WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_one_with_creator(cls, data):
        query = "SELECT * FROM users LEFT JOIN sasquatch ON users.id = sasquatch.users_id WHERE sasquatch.users_id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        one_show = cls(result[0])
        creator_info = {
            'id':result[0]['users_id'],
            'first_name':result[0]['first_name'],
            'last_name':result[0]['last_name'],
            'email':result[0]['email'],
            'password':result[0]['password'],
            'create_at':result[0]['create_at'],
            'upload_at':result[0]['upload_at'],
        }
        one_user = users.User(creator_info)
        one_show.creator = one_user
        return one_show

    @classmethod
    def update(cls, data):
        query = "UPDATE sasquatch SET location=%(location)s, happend=%(happend)s, count=%(count)s, date=%(count)s, update_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM sasquatch WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(sasquatch):
        is_valid = True
        if len(sasquatch['location']) < 1:
            is_valid = False
            flash("Location must be at least 3 characters","sasquatch")
        if len(sasquatch['happend']) < 3:
            is_valid = False
            flash("Happend must be at least 3 characters","sasquatch")
        if sasquatch['date'] == "":
            is_valid = False
            flash("Please enter a date","sasquatch")
        if int(sasquatch['count']) < 1:
            is_valid = False
            flash("Please use a vaild number","sasquatch")
        return is_valid