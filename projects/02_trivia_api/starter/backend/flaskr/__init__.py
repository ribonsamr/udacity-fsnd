import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = QUESTIONS_PER_PAGE * (page - 1)
    end = QUESTIONS_PER_PAGE + start

    questions = selection
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
        return jsonify({'success': True, 'categories': categories})

    @app.route('/questions')
    def get_questions():
        questions = paginate_questions(
            request,
            Question.query.order_by(Question.id).all())
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

        if not q:
            abort(404)

        q.delete()
        return jsonify({
            'success': True,
        }), 200

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        q = Question(body['question'], body['answer'], body['category'],
                     body['difficulty'])
        q.insert()
        return jsonify({'success': True, 'id': q.id}), 200

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.get_json()['searchTerm']
        questions = [
            q.format() for q in Question.query.order_by(Question.id).filter(
                Question.question.ilike(f"%{search_term}%")).all()
        ]
        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': ''
        }), 200

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

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        previous_questions = body['previous_questions']  # By ID
        quiz_category = int(body['quiz_category']['id'])

        # If ALL
        if quiz_category == 0:
            questions = [q.format() for q in Question.query.all()]

            # Don't choose from previous questions
            questions = list(
                filter(lambda x: int(x['id']) not in previous_questions,
                       questions))

            # If there's no questions left, force end
            if not questions:
                return jsonify({'success': True, 'forceEnd': True})

            question = random.choice(questions)
            return jsonify({'success': True, 'question': question})

        else:
            questions = [
                q.format() for q in Question.query.join(
                    Category, Question.category == Category.id).filter(
                        Category.id == quiz_category).all()
            ]

            # Don't choose from previous questions
            questions = list(
                filter(lambda x: int(x['id']) not in previous_questions,
                       questions))

            # If there's no questions left, force end
            if not questions:
                return jsonify({'success': True, 'forceEnd': True})

            question = random.choice(questions)
            return jsonify({'success': True, 'question': question})

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
