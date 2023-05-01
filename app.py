"""Flask app for Cupcakes"""
import os

from flask import Flask, render_template, redirect, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_homepage():

    return 'hi'

@app.get('/api/cupcakes')
def list_all_cupcakes():
    """return a list of all cupcakes as JSON objects
    {cupcakes: [{id, flavor, size, rating, image_url}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """return a single cupcake JSON object
    {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def add_cupcake():
    """
    add a single cupcake to Cupcakes
    Return a json object of added cupcake
    {cupcake: {id, flavor, size, rating, image_url}}
    """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    #could do if statement here,
    image_url = request.json.get('image_url') or None

    new_cupcake = Cupcake(flavor=flavor, size=size,
                          rating=rating, image_url=image_url)

    db.session.add(new_cupcake)
    #try to commit, accept data error if DB error
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupacake(cupcake_id):
    """
    update a single cupcake
    Return a json object of updated cupcake
    {cupcake: {id, flavor, size, rating, image_url}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

# Add "or" into get statements
    cupcake.flavor = request.json.get('flavor') or cupcake.flavor
    cupcake.size = request.json.get('size') or cupcake.size
    cupcake.rating = request.json.get('rating') or cupcake.rating
    #could do if statement here,
    cupcake.image_url = request.json.get('image_url') or cupcake.image_url

    #does key exist in JSON
    #update the image URL to either what we get back or default image

    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake = serialized), 200)

@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """
    delete a single cupcake
    Return a json object of updated cupcake
    {deleted: [cupcake-id]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(deleted = cupcake_id), 200)






