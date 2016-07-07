from models.shared import db

class Cocktail_Ingredient(db.Model):
	__tablename__ = 'cocktail_ingredients'

	id = db.Column(db.Integer, primary_key=True)
	cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'), primary_key=True)
	ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
	amount = db.Column(db.Text, nullable=False)
	ingredient = db.relationship('Ingredient', back_populates='cocktails')
	cocktail = db.relationship('Cocktail', back_populates='ingredients')
	
	def __init__ (self, id, cocktail_id, ingredient_id, amount):
		self.id = id
		self.cocktail_id = cocktail_id
		self.ingredient_id = ingredient_id
		self.amount = amount