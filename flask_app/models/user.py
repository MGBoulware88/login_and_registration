from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
import re


class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

############# INSERT USER INTO DB
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query, data)
    
############# GRAB EVERY USER FROM DB    
    @classmethod
    def read_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DB).query_db(query)
        users_list = []
        for user in results:
            users_list.append(cls(user))
        return users_list

############# GRAB 1 USER BY ID  
    @classmethod
    def read_one_user_by_id(cls, id):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        data = {
            'id':id
        }
        results = connectToMySQL(DB).query_db(query, data)
        return cls(results[0])

############# GRAB 1 USER BY EMAIL
    @classmethod
    def read_one_user_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            'email':email
        }
        results = connectToMySQL(DB).query_db(query, data)
        if not len(results):
            return False
        
        return cls(results[0])
    
############# VALIDATE REG FORM INPUTS
    @staticmethod
    def validate_reg(data):
        regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')
        email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,7}\b')
        is_valid = True # we assume this is true
        
        # first name must be >2 char and contain no special char
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'reg')
            is_valid = False
        if  regex.match(data['first_name']):
            flash("First Name cannot contain special characters.", 'reg')
            is_valid = False

        # last name must be >2 char and contain no special char
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 3 characters.", 'reg')
            is_valid = False
        if regex.match(data['last_name']):
            flash("Last Name cannot contain special characters.", 'reg')
            is_valid = False

        # email must be a valid email and not already taken
        if not email_regex.match(data['email']):
            flash("Invalid email address.", 'reg')
            is_valid = False
        else:
            email_taken = User.read_one_user_by_email(data['email'])
            if email_taken:
                is_valid = False
                return flash("Email already taken! Please try to login instead.", 'reg')
        
        # password must be >7 char and match confirm password
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", 'reg')
            is_valid = False
        elif not data['password'] == data['confirm_password']:
            flash("Both Password fields must match!", 'reg')
            is_valid = False
        
        # return T/F after checking all inputs for validity
        return is_valid