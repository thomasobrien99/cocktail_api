from models.shared import db

class Cocktail(db.Model):
	__tablename__ = 'cocktails'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	recipe = db.Column(db.Text, nullable=False)
	category = db.Column(db.Text, nullable=False)
	alcoholic = db.Column(db.Boolean, nullable=False)
	glass = db.Column(db.Text, nullable=False)
	ingredients = db.relationship('Cocktail_Ingredient', back_populates='cocktail')

	def __init__ (self, id, name, recipe, category, alcoholic, glass):
		self.id = id
		self.name = name
		self.recipe = recipe
		self.category = category
		self.alcoholic = alcoholic
		self.glass = glass
