import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()


## ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    drinks = [d.short() for d in drinks]

    return jsonify({'success': True, 'drinks': drinks}), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(p):
    drinks = Drink.query.all()
    drinks = [d.long() for d in drinks]

    return jsonify({'success': True, 'drinks': drinks}), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(p):
    res = request.get_json()

    if not res:
        abort(422)

    title = res.get('title', '')
    recipe = json.dumps(res.get('recipe', '{}'))

    drink = Drink(title=title, recipe=recipe)

    try:
        drink.insert()
    except:
        print(sys.exc_info())
        abort(422)

    drinks = [d.long() for d in Drink.query.all()]

    return jsonify({'success': True, 'drinks': drinks}), 200


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(p, drink_id):
    d = Drink.query.get(drink_id)

    if not d:
        abort(404)

    res = request.get_json()

    if not res:
        abort(422)

    d.title = res.get('title', '')
    d.recipe = json.dumps(res.get('recipe', '{}'))

    try:
        d.update()
    except:
        print(sys.exc_info())
        abort(422)

    return jsonify({'success': True, 'drinks': d.long()}), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(p, drink_id):
    d = Drink.query.get(drink_id)

    if not d:
        abort(404)

    d_id = d.id

    try:
        d.delete()
    except:
        print(sys.exc_info())
        abort(422)

    return jsonify({'success': True, 'delete': d_id}), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


# Handle AuthErrors
@app.errorhandler(AuthError)
def autherror_handler(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
