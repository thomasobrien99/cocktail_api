from models.shared import db

class Ingredient(db.Model):
	__tablename__ = 'ingredients'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	cocktails = db.relationship('Cocktail_Ingredient', back_populates='ingredient')
	def __init__ (self, id, name):
		self.id = id
		self.name = name