import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])
        # self.assertTrue(len(data['questions']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=10', json={'category': 1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_categories(self):
        res = self.client().get('/api/v1.0/categories')
        # data = json.loads(res.data)
        categories = Category.query.all()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(categories['id'], 1)
        self.assertEqual(categories['type'], "History")
       
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/56', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')
        
    
    def test_delete_question(self):
        res = self.client().delete('/question/2')
        data = json.loads(res.data)
        
        question = Question.query.filter(Question.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)
    
    def test_422_delete_question_failed(self):
        res = self.client().delete('/question/500')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        
    def test_create_new_question(self):
        res = self.client().post('/question', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_405_if_creation_not_allowed(self):
        res = self.client().post('/questions/56', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()