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

@app.route('/recipes', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()

            recipe_title = data['title']
            recipe_ingredients = data['ingredients']
            recipe_instructions = data['instructions']

            new_recipe = Recipes(title=recipe_title, ingredients=recipe_ingredients, method=recipe_instructions)

            try:
                db.session.add(new_recipe)
                db.session.commit()

                if request.headers.get('Accept') == 'application/json':
                    return jsonify({'message': 'Recipe created successfully'})
                else:
                    return redirect('/')
            except Exception as e:
                error_message = 'Failed to create recipe: ' + str(e)
                if request.headers.get('Accept') == 'application/json':
                    return jsonify({'message': error_message})
                else:
                    return render_template('error.html', message=error_message)
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
                return render_template('error.html', message='Failed to add the recipe.')
    elif request.method == 'GET':
        if request.headers.get('Accept') == 'application/json':
            recipes = Recipes.query.all()
            recipe_list = []
            for recipe in recipes:
                recipe_data = {
                    'id': recipe.id,
                    'title': recipe.title,
                    'ingredients': recipe.ingredients,
                    'instructions': recipe.method
                }
                recipe_list.append(recipe_data)
            return jsonify(recipe_list)
        else:
            return render_template('add_recipes.html')
    else:
        return "Method not allowed"
    
    
# @app.route('/update_recipe/<int:recipe_id>', methods=['GET','POST'])
# def update_recipe(recipe_id):
#     recipe = Recipes.query.get_or_404(recipe_id)

#     if request.method == 'POST':
#         if request.content_type == 'application/json':
#             data = request.get_json()

#             recipe.title = data.get('title', recipe.title)
#             recipe.ingredients = data.get('ingredients', recipe.ingredients)
#             recipe.method = data.get('instructions', recipe.method)

#             try:
#                 db.session.commit()
#                 return jsonify({'message': 'Recipe updated successfully'})
#             except Exception as e:
#                 return jsonify({'message': 'Failed to update recipe', 'error': str(e)})
#         else:
#             recipe.title = request.form.get('title', recipe.title)
#             recipe.ingredients = request.form.get('ingredients', recipe.ingredients)
#             recipe.method = request.form.get('instructions', recipe.method)

#             try:
#                 db.session.commit()
#                 return redirect('/')
#             except Exception as e:
#                 return "There was an issue updating your recipe."
#     else:
#         return render_template('update_recipe.html', recipe=recipe)

# @app.route('/delete_recipe/<int:recipe_id>', methods=['GET','DELETE','POST'])
# def delete_recipe(recipe_id):
#     recipe_to_be_deleted = Recipes.query.get_or_404(recipe_id)
    
#     if request.method == 'DELETE':
#         try:
#             db.session.delete(recipe_to_be_deleted)
#             db.session.commit()
#             return jsonify({'message': 'Recipe deleted successfully'})
#         except Exception as e:
#             return jsonify({'message': 'Failed to delete recipe', 'error': str(e)})
#     else:
#         try:
#             db.session.delete(recipe_to_be_deleted)
#             db.session.commit()
#             return redirect('/')
#         except Exception as e:
#             return "There was a problem deleting that record"
    
@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)

    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
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
    
    elif request.method == 'PUT':
        if request.headers.get('Content-Type') == 'application/json':
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
            return "PUT method not supported for HTML form submissions."
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(recipe)
            db.session.commit()
            
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'message': 'Recipe deleted successfully'})
            else:
                return redirect('/')
        
        except Exception as e:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'message': 'Failed to delete recipe', 'error': str(e)})
            else:
                return "There was a problem deleting that record"
    
    else:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({
                'title': recipe.title,
                'ingredients': recipe.ingredients,
                'instructions': recipe.method
            })
        else:
            return render_template('update_recipe.html', recipe=recipe)



@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        recipe =  Recipes.query.filter(or_(Recipes.title.like(f'%{query}%'))).first()
        if recipe:
            if request.headers.get('Content-Type') == 'application/json':
                # Return a JSON response for API requests
                return jsonify({'recipe_title': recipe.title, 'recipe_ingredients': recipe.ingredients, 'recipe_instructions': recipe.method})
            else:
                return render_template('view_recipe.html', recipe=recipe)
        else:
            flash('No matching recipe found.')
            return redirect('/')
    
    # If no matching recipe is found or the query is empty, handling the response accordingly
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'message': 'No matching recipe found.'})
    else:
        flash('Please enter a search query.')
        return redirect('/')

if __name__=="__main__":
    app.run(debug=True)