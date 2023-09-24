from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import recipe, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboards():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("recipe_dashboard.html", recipe = recipe.Recipe.get_all_user_recipe(), user = user.Person.user_get_id(data))

@app.route('/recipe/add', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    valid = recipe.Recipe.recipe_validate(request.form)
    if valid:
        data = {
            'name': request.form['name'],
            'ingredients': request.form['ingredients'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'user_id': session['user_id']
        }
        recipes = recipe.Recipe.create_recipe(data)
        return redirect('/dashboard')
    return redirect('/add/recipe')

@app.route('/add/recipe')
def add_new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template("recipe_add.html", user = user.Person.user_get_id(data))

@app.route('/recipe/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    return render_template("recipe_edit.html", recipe = recipe.Recipe.get_a_recipe(data))

@app.route('/recipes/<int:recipe_id>/edit_in_db', methods = ['POST'])
def edit_your_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    if not recipe.recipe.recipe_validate(request.form):
        data = {
            'title': request.form['title'],
            'ingredients': request.form['ingredients'],
            'description': request.form['description'],
            'id': session['user_id']
        }
        recipes = recipe.recipe.update_recipe(data)
        return redirect('/dashboard')
    return redirect('/recipe/<int:recipe_id>/edit')

@app.route('/recipe/<int:recipe_id>/update', methods = ['POST'])
def update_recipe(recipe_id):
    recipe.Recipe.update_recipe(request.form)
    return redirect('/dashboard')

@app.route('/show/<int:recipe_id>/')
def show_recipe_info(recipe_id):
    data = {
        'id': recipe_id
    }
    return render_template("recipe_show.html", recipe = recipe.Recipe.get_one_user_recipe(data))

@app.route('/recipe/<int:id>/delete')
def delete(id):
    data = {
        "id": id
    }
    recipe.recipe.delete_recipe(data)
    return redirect('/dashboard')