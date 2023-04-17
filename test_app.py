import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import Actor, Movie

load_dotenv()

# Getting values from .env file
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')

casting_assistant_token = {'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJrYU5wcjZVN1F3N3dOWkxKQW9fZyJ9.eyJpc3MiOiJodHRwczovL3Jhc2hpZC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDMzNzk3M2FmY2FiYWVlYTZlOGNmODAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY4MTY0NTQ0NCwiZXhwIjoxNjgxNjUyNjQ0LCJhenAiOiJYbVhtZVpIdFZxMlRXNk90N1FERXR5MVpiS2UxeDdLOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.vecMW0MjOc__yiNXpkQGYxKKaOyyITCJnG1Haq293dlQfJalAXP_ge5ncAf4CTYkDWBNaIxqR9AjPXqvdQmMZ-2SAJUFjk88NxB91CdzwKWnQ7KUeQ3xq6YytcrwZHq-S0wadYQaYRI6Q4Fuq7tMS8uqjVEO0IqmNr4My5qO-TI6cF9z8DBCUpI8hOWXvZoG6PnaJp2TxWLl94zOqdgEBruFRrnbG8KS76-u3SQzj1UZbatvG8O2Nl5oq8xcAW7fVZg5eYzQMOjrFCCJMUu4BEE_OO3EpS7X023MoL06229BCASUtmkTv9LsbMRk1fyCUV1m6Aos3FqX5GWwvP3IOg'}
casting_director_token  = {'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJrYU5wcjZVN1F3N3dOWkxKQW9fZyJ9.eyJpc3MiOiJodHRwczovL3Jhc2hpZC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDMzNGRjNzUyZmI3NjdmN2VhZWJjYzgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY4MTY0NjQ5MSwiZXhwIjoxNjgxNjUzNjkxLCJhenAiOiJYbVhtZVpIdFZxMlRXNk90N1FERXR5MVpiS2UxeDdLOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.wXZ1ofuEl1O9FIdM_aehhGxdNzQzMFSXIxRI-CA9NzoVvSpiGsfjaNrs5tDyZOmnCviLW4ai9gq58sOa6okF8IWLlKmcOg1Y0_DZWV7Ue28J2iNWT_iewo20RP3FOuJ5Xfn3oXE7YxzfDnLF-8wX2WHqoBSze2Pv-f-L7AEE5lmtpGKRE762S9RlFIHRXim0ufnxEQRLAZ8mHLP7bsgrGBPykMucLyGeeNnpmljmROwoBPWahlxZjnICw5Wz14PjlruwnV3GZuJVn6d8M2bgbUp9Koy7LUXMM3PNk5XeUQruMycceDoSVWFlmz0Bl9NyexxdqNw3fcPP5wNDKR2xaQ'}
casting_executive_token = {'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJrYU5wcjZVN1F3N3dOWkxKQW9fZyJ9.eyJpc3MiOiJodHRwczovL3Jhc2hpZC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDNiYjM4Njc3ZmIxMjVlZjI5OTQ2NjAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY4MTY0NjU0MywiZXhwIjoxNjgxNjUzNzQzLCJhenAiOiJYbVhtZVpIdFZxMlRXNk90N1FERXR5MVpiS2UxeDdLOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.Jwn6ygYLo4gZ32cVDOu5ttdRp3xyc8RxG-zV_70eNqMeNbbAx3eK9Kz2VH6BSpYaQAWonPtWpIJXTHuK7jmrW1v17mcdRQPoMsuXg2qCXGVkwN3QuFYBHTHvP-Y5On5yvOc1oIdCtLb15ZzncXELkVtV9OaLdIHvouHRnasLaT23BtXeWeYbe9XBosQ_SHI_AGnXpfpnE-m6sGOgrH88Ar3qh5GJ5klrsXmFVSibDCtHy38FxyYIWUaxdyGgbH-35vZup_V0viTWB9t7BKFC7YsGcqBHyZIgkaP1Wk7MifFSFE2xMK_yJKalHr801o1FusPgoJ2uzQ3CMwelz0XM5g'}


class CapstoneTest(unittest.TestCase):
    # Class represents the test case

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

    def setup_db(app):
        db = SQLAlchemy()
        database_path = 'postgresql://{}:{}@{}:{}/{}'.format(
            user, password, 'localhost', 5432, database_name)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO: Done
    # TODO: One test for success behavior of each endpoint :DONE
    # TODO: One test for error behavior of each endpoint   :DONE
    # TODO: At least two tests of RBAC for each role       :DONE
    """
    
    # Casting Assistant - Get Actors 
    def test_get_paginated_actors(self):
        result = self.client().get('/actors', headers=casting_assistant_token)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # Casting Assistant - Get Actors without valid jwt
    def test_401_paginated_actors(self):
        result = self.client().get('/actors')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        
    # Casting Director - Delete actors #will run only once unless we change the id to delete
    def test_delete_actors(self):
                
        result = self.client().delete(f'/actors/2', headers=casting_director_token)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # Unauthorized delete - 401
    def test_401_delete_actors(self):
                
        result = self.client().delete(f'/actors/1')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        
        
    # Casting Director - Add actors   
    def test_add_actors(self):
        actor = {
            'name': 'Tom Cruise',
            'age': 60,
            'gender': 'M',
            'movie_id': 2
        }

        result = self.client().post('/actors', headers=casting_director_token, json=actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
    
    # Add actor without permission
    def test_401_add_actors(self):
        actor = {
            'name': 'Tom Cruise',
            'age': 60,
            'gender': 'M',
            'movie_id': 2
        }

        result = self.client().post('/actors', json=actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["success"], False)
    
    
    # Casting Director - Update actors   
    def test_update_actors(self):
        actor = {
            'name': 'Tom Holland',
            'age': 26,
            'gender': 'M',
            'movie_id': 1
        }

        result = self.client().patch('/actors/1', headers=casting_director_token, json=actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
    
    
    # Update actors 401   
    def test_401_update_actors(self):
        actor = {
            'name': 'Tom Holland',
            'age': 26,
            'gender': 'M',
            'movie_id': 1
        }

        result = self.client().patch('/actors/1', json=actor)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["success"], False)
    
    
    # Casting Assistant - Get movies 
    def test_get_movies(self):
        result = self.client().get('/movies', headers=casting_assistant_token)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # Casting Assistant - Get movies without valid jwt
    def test_401_get_movies(self):
        result = self.client().get('/movies')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
    
    
    # Casting Executive - Delete movies #will run only once unless we change the id to delete
    def test_delete_movies(self):
                
        result = self.client().delete(f'/movies/2', headers=casting_executive_token)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # Unauthorized delete movies - 401
    def test_401_delete_movies(self):
                
        result = self.client().delete(f'/movies/2')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data['success'], False)
        
        
    # Casting Executive - Add movies   
    def test_add_movies(self):
        movie = {
            'title': 'Test Movie',
            'release_date': '20200202'
        }

        result = self.client().post('/movies', headers=casting_executive_token, json=movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
    
    # Add movie without permission
    def test_401_add_movies(self):
        movie = {
            'title': 'Test Movie',
            'release_date': '20200202'
        }

        result = self.client().post('/movies', json=movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["success"], False)
        
    
    # Casting Executive - Update movies   
    def test_update_movies(self):
        movie = {
            'title': 'Updated title',
            'release_date': '20200202'
        }

        result = self.client().patch('/movies/3', headers=casting_director_token, json=movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
    
    
    # Update movie 401   
    def test_401_update_movies(self):
        movie = {
            'title': 'Updated title',
            'release_date': '20200202'
        }

        result = self.client().patch('/movies/3', json=movie)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(data["success"], False)
        
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
