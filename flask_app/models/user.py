# Login Registration Assignment
# Author: Vignesh Manickam

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_user_by_email(cls,user_email):
        data = {"email":user_email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('users_registration').query_db(query,data)
        if len(results) < 1 :
            return False
        return cls(results[0])
    
    @classmethod
    def add_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        results = connectToMySQL('users_registration').query_db(query,data)
        return results
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name should have atleast 2 Characters","register")
            is_valid = False
        if len(user['last_name']) < 2 :
            flash("Last Name should have atleast 2 Characters","register")
            is_valid = False
        if len(user['email']) == 0 :
            flash("Email cannot be empty","register")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address","register")
            is_valid = False
        if len(user['password']) < 8 :
            flash("Password should have atleast 8 Characters","register")
            is_valid = False
        elif not PASSWORD_REGEX.match(user['password']):
            flash("Password should contain atleast 1 Upper case and 1 Number","register")
            is_valid = False
        if len(user['confirm_password']) < 8 :
            flash("Confirm Password should have atleast 8 Characters","register")
            is_valid = False
        if not (user['password'] == user['confirm_password']) :
            flash("Password and Confirm Password is NOT matching","register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) == 0 :
            flash("Email cannot be empty","login")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address","login")
            is_valid = False
        if len(user['password']) == 0 :
            flash("Password cannot be empty","login")
            is_valid = False
        return is_valid