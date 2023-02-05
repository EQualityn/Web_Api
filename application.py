from flask import Flask, request
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
# with app.app_context():
#     db.create_all()
# app.app_context().push()
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True,nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/meals')
def get_meals():
    meals = Meal.query.all()
    out = []
    for meal in meals:
        meal_data = {'name': meal.name, 
        'description': meal.description}
        out.append(meal_data)
    
    return {"meals": out}
@app.route('/meals/<id>')
def get_meal(id):
    meal = Meal.query.get_or_404(id)
    return {"name": meal.name, "description": meal.description}

@app.route('/meal', methods=['POST'])
def add_meal():
    meal = Meal(name=request.json['name'], description=request.json['description'])
    db.session.add(meal)
    db.session.commit()
    return {'id': meal.id}
@app.route('/meals/<id>', methods=['DELETE'])
def delete_meal():
    meal = Meal.query.get(id)
    if meal is None:
        return {"error": "not found"}
    db.session.delete(meal)
    db.session.commit()
    return {"message": "Delete success!"}