from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from marshmallow import Schema, fields
from models.shared import db
from models.cocktails import Cocktail
from models.ingredients import Ingredient
from models.cocktail_ingredients import Cocktail_Ingredient
import json

app = Flask(__name__)
api = Api(app)
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/cocktails_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class CocktailSchema(Schema):
	id = fields.Integer()
	name = fields.String()
	recipe = fields.String()
	category = fields.String()
	glass = fields.String()
	alcoholic = fields.Boolean()
	ingredients = fields.Nested('IngredientSchema', many=True, exclude=('cocktails'))
	
class IngredientSchema(Schema):
	id = fields.Integer()
	name = fields.String()
	ingredient = fields.String()
	cocktails = fields.Nested(CocktailSchema, many=True, exclude=('ingredients'))


class CocktailApi(Resource):
	def get(self, id):
		return c_schema.dump(Cocktail.query.get(id))

class CocktailListApi(Resource):
	def get(self):
		return c_schema.dump(Cocktail.query.all(), many=True)

class IngredientApi(Resource):
	def get(self, id):
		return i_schema.dump(Ingredient.query.get(id))

class IngredientListApi(Resource):
	def get(self):
		return i_schema.dump(Ingredient.query.all(), many=True)


api.add_resource(CocktailListApi, '/api/cocktails/')
api.add_resource(CocktailApi, '/api/cocktails/<int:id>')
api.add_resource(IngredientListApi, '/api/ingredients/')
api.add_resource(IngredientApi, '/api/ingredients/<int:id>')


# for reading data into tables
# cocktail_txt = open('./saved_cocktail_data/cocktail_list','r')
# ingredient_txt = open('./saved_cocktail_data/ingredient_list','r')
# cocktail_ingredient_list = open('./saved_cocktail_data/cocktail_ingredient_list','r')

# cocktails = json.load(cocktail_txt)["data"]
# ingredients = json.load(ingredient_txt)["data"]
# cocktail_ingredients = json.load(cocktail_ingredient_list)["data"]



# for x in range(0, len(cocktail_ingredients)):
# 	# new_Cocktail = Cocktail(int(cocktails[x]["id"]), cocktails[x]["name"], cocktails[x]["recipe"], cocktails[x]["category"], cocktails[x]["alcoholic"], cocktails[x]["glass"])
# 	# new_ingredient = Ingredient(int(ingredients[x]["id"]), ingredients[x]["name"])
# 	new_cocktail_ingredient = Cocktail_Ingredient(cocktail_ingredients[x]["id"], cocktail_ingredients[x]["cocktail_id"], cocktail_ingredients[x]["ingredient_id"], cocktail_ingredients[x]["amount"])
# 	db.session.add(new_cocktail_ingredient)
# 	db.session.commit()


if __name__ == '__main__':
	app.run(debug=True, port=3000)