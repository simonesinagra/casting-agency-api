import os
import unittest
import json

from api import create_app
from settings import CASTING_ASSISTANT_TOKEN, CASTING_DIRECTOR_TOKEN, EXECUTIVE_PRODUCER_TOKEN

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })
        self.client = self.app.test_client

        # Sample actor and movie data
        self.new_actor = {
            'name': 'Test Actor',
            'age': 30,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Test Movie',
            'release_date': '2020-08-15T00:00:00+0000'
        }

        # Tokens for different roles
        self.assistant_token = f'Bearer {CASTING_ASSISTANT_TOKEN}'
        self.director_token = f'Bearer {CASTING_DIRECTOR_TOKEN}'
        self.producer_token = f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test for getting actors
    def test_get_actors(self):
        """Test getting all actors"""
        res = self.client().get('/actors', headers={"Authorization": self.assistant_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    # Test for getting movies
    def test_get_movies(self):
        """Test getting all movies"""
        res = self.client().get('/movies', headers={"Authorization": self.assistant_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    # Test for adding a new actor
    def test_add_actor(self):
        """Test adding a new actor"""
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data)

    # Test for adding a new movie
    def test_add_movie(self):
        """Test adding a new movie"""
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": self.producer_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data)

    # Test for updating an actor
    def test_update_actor(self):
        """Test updating an actor's information"""
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        actor_id = data['created']

        updated_actor = {
            'name': 'Updated Actor Name',
            'age': 35,
            'gender': 'Female'
        }
        res = self.client().patch(f'/actors/{actor_id}', json=updated_actor, headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    # Test for updating a movie
    def test_update_movie(self):
        """Test updating a movie's information"""
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": self.producer_token})
        data = json.loads(res.data)
        movie_id = data['created']

        updated_movie = {
            'title': 'Updated Movie Title',
            'release_date': '2025-01-01'
        }
        res = self.client().patch(f'/movies/{movie_id}', json=updated_movie, headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    # Test for deleting an actor
    def test_delete_actor(self):
        """Test deleting an actor"""
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        actor_id = data['created']

        res = self.client().delete(f'/actors/{actor_id}', headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)

    # Test for deleting a movie
    def test_delete_movie(self):
        """Test deleting a movie"""
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": self.producer_token})
        data = json.loads(res.data)
        movie_id = data['created']

        res = self.client().delete(f'/movies/{movie_id}', headers={"Authorization": self.producer_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)

    # Test RBAC: Casting Assistant cannot add actors
    def test_casting_assistant_cannot_add_actor(self):
        """Test that Casting Assistant cannot add actors"""
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": self.assistant_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Permission not found.")

    # Test RBAC: Casting Director cannot delete movies
    def test_casting_director_cannot_delete_movie(self):
        """Test that Casting Director cannot delete movies"""
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": self.producer_token})
        data = json.loads(res.data)
        movie_id = data['created']

        res = self.client().delete(f'/movies/{movie_id}', headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["message"], "Permission not found.")

    # Error behavior tests

    def test_404_if_actor_does_not_exist(self):
        """Test error if actor does not exist"""
        res = self.client().get('/actors/1000', headers={"Authorization": self.assistant_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_400_if_actor_creation_fails(self):
        """Test error if actor creation fails due to missing data"""
        incomplete_actor = {
            'name': 'Incomplete Actor'
        }
        res = self.client().post('/actors', json=incomplete_actor, headers={"Authorization": self.director_token})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()