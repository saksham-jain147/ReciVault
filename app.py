from flask import Flask, render_template, jsonify, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    method = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return f'Title : {self.name}'


@app.route('/')
def index():
    recipes = Recipes.query.order_by(Recipes.id).all()
    return render_template('index.html', recipes=recipes)

@app.route('/recipes', methods=['GET','POST'])
def create_recipe():
    if request.method== 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()

            recipe_title = data['title']
            recipe_ingredients = data['ingredients']
            recipe_instructions = data['instructions']

            new_recipe = Recipes(title=recipe_title, ingredients=recipe_ingredients, method=recipe_instructions)

            try:
                db.session.add(new_recipe)
                db.session.commit()
                return jsonify({'message': 'Recipe created successfully'})
            except Exception as e:
                return jsonify({'message': 'Failed to create recipe', 'error': str(e)})
        else:
            recipe_title = request.form['title']
            recipe_ingredients = request.form['ingredients']
            recipe_instructions = request.form['instructions']

            new_recipe = Recipes(title=recipe_title, ingredients=recipe_ingredients, method=recipe_instructions)

            try:
                db.session.add(new_recipe)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                return "There was an issue adding your recipe"
    else:
        return render_template('add_recipes.html')

# @app.route('/recipes/<recipe_id>', methods=['GET'])
# def get_recipe(recipe_id):
#     # Logic to retrieve the specified recipe
#     return jsonify({'recipe': recipe})

@app.route('/update_recipe/<int:recipe_id>', methods=['GET','POST'])
def update_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)

    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()

            recipe.title = data.get('title', recipe.title)
            recipe.ingredients = data.get('ingredients', recipe.ingredients)
            recipe.method = data.get('instructions', recipe.method)

            try:
                db.session.commit()
                return jsonify({'message': 'Recipe updated successfully'})
            except Exception as e:
                return jsonify({'message': 'Failed to update recipe', 'error': str(e)})
        else:
            recipe.title = request.form.get('title', recipe.title)
            recipe.ingredients = request.form.get('ingredients', recipe.ingredients)
            recipe.method = request.form.get('instructions', recipe.method)

            try:
                db.session.commit()
                return redirect('/')
            except Exception as e:
                return "There was an issue updating your recipe."
    else:
        return render_template('update_recipe.html', recipe=recipe)

@app.route('/delete_recipe/<int:recipe_id>', methods=['GET','DELETE','POST'])
def delete_recipe(recipe_id):
    recipe_to_be_deleted = Recipes.query.get_or_404(recipe_id)
    
    if request.method == 'DELETE':
        try:
            db.session.delete(recipe_to_be_deleted)
            db.session.commit()
            return jsonify({'message': 'Recipe deleted successfully'})
        except Exception as e:
            return jsonify({'message': 'Failed to delete recipe', 'error': str(e)})
    else:
        try:
            db.session.delete(recipe_to_be_deleted)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return "There was a problem deleting that record"
    
    

@app.route('/view_recipe/<string:recipe_title>', methods=['GET'])
def view_recipe(recipe_title):
    recipe = Recipes.query.filter_by(title=recipe_title).first_or_404()

    return render_template('view_recipe.html', recipe=recipe)
    # Logic to search for recipes based on criteria
    # return jsonify({'results': recipes})

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Perform the search in the database based on the query
        # Here, you can use the query to search for the recipe name in the database
        # If a matching recipe is found, redirect to the view_recipe page for that recipe
        # For example:
        # recipe = Recipes.query.filter_by(title=query).first()
        recipe =  Recipes.query.filter(or_(Recipes.title.like(f'%{query}%'))).first()
        if recipe:
            return render_template('view_recipe.html', recipe=recipe)
        else:
            flash('No matching recipe found.')
            return redirect('/')
    
    # If no matching recipe is found or the query is empty, redirecting to home page
    flash('Please enter a search query.')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)