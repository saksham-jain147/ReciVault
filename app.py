from flask import Flask, render_template, jsonify, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
        recipe_title = request.form['title']
        recipe_ingredients = request.form['ingredients']
        recipe_instructions = request.form['instructions']
        new_recipe = Recipes(title = recipe_title, ingredients = recipe_ingredients, method = recipe_instructions)
        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your recipe"
    # render_template('add_recipes.html')
    # return jsonify({'message': 'Recipe created successfully'})
    else:
        return render_template('add_recipes.html')

@app.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # Logic to retrieve the specified recipe
    return jsonify({'recipe': recipe})

@app.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    # Logic to update the specified recipe
    return jsonify({'message': 'Recipe updated successfully'})

@app.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    # Logic to delete the specified recipe
    return jsonify({'message': 'Recipe deleted successfully'})

@app.route('/recipes', methods=['GET'])
def search_recipes():
    # Logic to search for recipes based on criteria
    return jsonify({'results': recipes})


if __name__=="__main__":
    app.run(debug=True)