import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

os.system("dropdb trivia_test &>/dev/null")
os.system("createdb trivia_test &>/dev/null")
os.system("psql trivia_test < trivia.psql &>/dev/null")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_all_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_404_get_all_questions(self):
        response = self.client().get('/questions?page=3010')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertFalse('questions' in data)

    def test_delete_question(self):
        before = Question.query.count()
        response = self.client().delete('/questions/10')
        data = json.loads(response.data)
        after = Question.query.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(before, after)

    def test_fail_delete_question(self):
        before = Question.query.count()
        response = self.client().delete('/questions/0')
        data = json.loads(response.data)
        after = Question.query.count()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        before = Question.query.count()
        response = self.client().post('/questions',
                                      json={
                                          'question': 'a',
                                          'answer': 'b',
                                          'category': '1',
                                          'difficulty': '5'
                                      })
        data = json.loads(response.data)
        after = Question.query.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('id' in data)
        self.assertEqual(Question.query.get(data['id']).question, 'a')
        self.assertEqual(Question.query.get(data['id']).answer, 'b')
        self.assertEqual(Question.query.get(data['id']).category, 1)
        self.assertEqual(Question.query.get(data['id']).difficulty, 5)
        self.assertGreater(after, before)

    def test_search_question(self):
        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('questions' in data)
        self.assertEqual(len(data['questions']), 2)

    def test_get_question_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('questions' in data)
        self.assertEqual(len(data['questions']), 3)

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()