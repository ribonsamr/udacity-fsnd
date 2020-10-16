import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request):
    page = request.args.get('page', 1, type=int)
    start = QUESTIONS_PER_PAGE * (page - 1)
    end = QUESTIONS_PER_PAGE + start

    questions = Question.query.order_by(Question.id).all()
    questions = [q.format() for q in questions][start:end]

    return questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories = [c.format() for c in categories]
        return jsonify(categories)

    @app.route('/questions')
    def get_questions():
        questions = paginate_questions(request)
        categories = [c.format() for c in Category.query.all()]
        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'current_category': categories[0].get('type'),
            'categories': categories,
            'total_questions': len(Question.query.all())
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        q = Question.query.get(question_id)
        q.delete()
        return jsonify({
            'success': True,
        }), 200

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        q = Question(body['question'], body['answer'], body['difficulty'],
                     body['category'])
        q.insert()
        return jsonify({'success': True}), 200

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = [
            q.format() for q in Question.query.join(
                Category, Question.category == Category.id).filter(
                    Category.id == category_id).all()
        ]
        return jsonify({
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': Category.query.get(category_id).type
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Not allowed"
        }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
