from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user

class Recipe:
    db = "recipe_database"
    def __init__(self, recipe):
        self.id = recipe['id']
        self.name = recipe["name"]
        self.ingredients = recipe['ingredients']
        self.description = recipe['description']
        self.instructions = recipe['instructions']
        self.created_at = ['created_at']
        self.updated_at = ['updated_at']
        self.user_id = ['user_id']
        self.creator = None

    @classmethod 
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, ingredients, description, instructions, user_id) VALUES (%(name)s, %(ingredients)s, %(description)s, %(instructions)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def update_recipe(cls, data):
        query = """
            UPDATE recipes SET name = %(name)s, ingredients = %(ingredients)s, description = %(description)s, instructions = %(instructions)s,
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod 
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def recipe_validate(data):
        is_valid = True
        query = "SELECT * FROM recipes WHERE name = %(name)s;"
        results = connectToMySQL("recipe_deal").query_db(query, data)
        if len(results) != 0:
            flash("")
            is_valid = False
        if data['name'] < 2:
            flash('The name of the recipe must be at least 2 characters.')
            is_valid = False
        if data['ingredients'] < 5:
            flash('ingredients must be at least 5 characters.')
            is_valid = False
        if len(data['description']) < 3:
            flash("Recipe description must be at least 3 characters.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("recipe instructions must be at least 3 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_user_recipe(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        recipes = connectToMySQL(cls.db).query_db(query)
        results = []
        for recipe in recipes:
            data = {
                'id':recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            get_all_recipe = cls()
            get_all_recipe.creator = user.Person(data)
            results.append(get_all_recipe)
        return results

    @classmethod
    def get_one_user_recipe(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        data ={
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at':results[0]['created_at'],
            'updated_at':results[0]['updated_at']
        }
        get_recipe = cls(results[0])
        get_recipe.creator = user.Person(data)
        return get_recipe

    @classmethod
    def get_a_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])