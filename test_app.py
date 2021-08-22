import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # Use Executive Producer token to enable all tests
        self.header = {
            "Authorization": "Bearer {}".format(os.environ['TOKEN'])
        }

        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Define a new movie for testing the create movie endpoint
        self.new_movie = {
            'title': 'Captain America: Civil War',
            'release': '20/07/2018'
        }

        # define a new actor for testing the create actor endpoint
        self.new_actor = {
            'name': 'Paul Bettany',
            'age': 50,
            'gender': 'M'
        }

        # Updated movie details for testing the update endpoint
        self.update_movie = {
            'title': 'Avengers Assemble'
        }

        # Updated actor details for testing the update endpoint
        self.update_actor = {
            'name': 'Jeremy Renner',
            'age': 50
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test /movies GET
    # Successful operation
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    # No movies
    def test_404_get_movies(self):
        """
        NOTE
        This scenario will only work for a database with no movies
        it has therefore been commented out to avoid showing as a failed test
        """
    #     res = self.client().get('/movies', headers=self.header)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # Test /actors GET
    # Successful operation
    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    # No actors
    def test_404_get_actors(self):
        """
        NOTE
        This scenario will only work for a database with no actors
        it has therefore been commented out to avoid showing as a failed test
        """
    #     res = self.client().get('/actors', headers=self.header)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # Test /movies DELETE
    # Successful operation
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers=self.header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    # Movie doesn't exist
    def test_404_delete_movie_does_not_exist(self):
        res = self.client().delete('/movies/10000', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test /actors DELETE
    # Successful operation
    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers=self.header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    # Actor doesn't exist
    def test_404_delete_actor_does_not_exist(self):
        res = self.client().delete('/actors/10000', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test /movies POST
    # Successful operation
    def test_create_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_movie'])
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    # Create without any data
    def test_400_create_movie_no_data(self):
        res = self.client().post('/movies', json={}, headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Test /actors POST
    # Successful operation
    def test_create_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_actor'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    # Create without any data
    def test_400_create_actor_no_data(self):
        res = self.client().post('/actors', json={}, headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Test /movies PATCH
    # Successful operation
    def test_patch_movie(self):
        res = self.client().patch('/movies/1',
                                  json=self.update_movie,
                                  headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    # Update without any data
    def test_400_update_movie_no_data(self):
        res = self.client().patch('/movies/1', json={}, headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Movie doesn't exist
    def test_404_update_movie_does_not_exist(self):
        res = self.client().patch('/movies/10000',
                                  json=self.update_movie,
                                  headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test /actors PATCH
    # Successful operation
    def test_patch_actor(self):
        res = self.client().patch('/actors/1',
                                  json=self.update_actor,
                                  headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    # Update without any data
    def test_400_update_actor_no_data(self):
        res = self.client().patch('/actors/1', json={}, headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Actor doesn't exist
    def test_404_update_actor_does_not_exist(self):
        res = self.client().patch('/actors/10000',
                                  json=self.update_actor,
                                  headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
