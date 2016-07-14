from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields
from models.shared import db
from models.cocktails import Cocktail
from models.ingredients import Ingredient
from models.cocktail_ingredients import Cocktail_Ingredient

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
	ingredients = fields.Nested('CocktailIngredientSchema', many=True, exclude=('cocktail'))

class CocktailIdSchema(Schema):
	id = fields.Integer()
	name = fields.String()
	
class IngredientSchema(Schema):
	id = fields.Integer()
	name = fields.String()
	ingredient = fields.String()
	cocktails = fields.Nested('CocktailIngredientSchema', many=True, exclude=('ingredient'))

class IngredientIdSchema(Schema):
	id = fields.Integer()
	name = fields.String()

class CocktailIngredientSchema(Schema):
	amount = fields.String()
	cocktail = fields.Nested(CocktailSchema, only=('name', 'id'))
	ingredient = fields.Nested(IngredientSchema, only=('name', 'id'))

c_schema = CocktailSchema()
i_schema = IngredientSchema()

cid_schema = CocktailIdSchema()
iid_schema = IngredientIdSchema()

class CocktailApi(Resource):
	def get(self, id):
		return c_schema.dump(Cocktail.query.get(id))

class CocktailListApi(Resource):
	def get(self):
		all_cocktails = Cocktail.query.all()
		filtered_cocktails =[]
		if 'filter' in request.args and request.args['filter'] == 'ingredients':
			ingredient_ids = [int(x) for x in request.args['params'].split('^') if x]
			
			test = Cocktail_Ingredient.query.all()
			test = [x.cocktail for x in test if x.ingredient_id in ingredient_ids]
			possible_cocktails= list(set(test))

			for x in possible_cocktails:
				if len(x.ingredients) > len(ingredient_ids):
					continue
				for y in range(0,len(x.ingredients)):
					if x.ingredients[y].ingredient_id not in ingredient_ids:
					  break
					if y == (len(x.ingredients) - 1):
						filtered_cocktails.append(x)
			
			if request.args['type'] == 'ids':
				return cid_schema.dump(filtered_cocktails, many=True)
			return c_schema.dump(filtered_cocktails, many=True)

		if 'filter' in request.args and request.args['filter'] == 'ids':
			cocktail_ids = [int(x) for x in request.args['params'].split('^') if x]
			while len(cocktail_ids):
				filtered_cocktails.append(Cocktail.query.get(cocktail_ids.pop()))
			if request.args['type'] == 'ids':
				return cid_schema.dump(filtered_cocktails, many=True)
			return c_schema.dump(filtered_cocktails, many=True)

		if 'type' in request.args and request.args['type'] == 'ids':
				return cid_schema.dump(all_cocktails, many=True)
		return c_schema.dump(all_cocktails, many=True)

class IngredientApi(Resource):
	def get(self, id):
		return i_schema.dump(Ingredient.query.get(id))

class IngredientListApi(Resource):
	def get(self):
		if 'filter' in request.args and request.args['filter'] == 'ids':
			id_params = [int(x) for x in request.args['params'].split('^') if x]
			test = [x for x in Ingredient.query.all() if x.id in id_params]
			return iid_schema.dump(test, many=True)

		if 'type' in request.args and request.args['type'] == 'ids':
			return iid_schema.dump(Ingredient.query.all(), many=True)
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