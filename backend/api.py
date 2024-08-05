import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from models import setup_db, db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)

    with app.app_context():
        if test_config is None:
            setup_db(app)
        else:
            database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
            setup_db(app, database_path=database_path)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH,OPTIONS"
        )
        return response

    # Routes

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        if(len(movies) == 0):
            abort(404)
        
        movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies
        }), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        if(len(actors) == 0):
            abort(404)

        actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()
        if(body is None):
            abort(422)

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        
        try:
            if not all([title, release_date]):
                abort(422)
            
            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify(
                {
                    "success": True,
                    "created": movie.id,
                }
            ), 201
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        body = request.get_json()
        if(body is None):
            abort(422)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            if not all([name, age, gender]):
                abort(422)
        
            
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify(
                {
                    "success": True,
                    "created": actor.id,
                }
            ), 201
        
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        try: 
            movie.delete()

        except:
            abort(422)

        return jsonify({
            "success": True,
            "deleted": movie_id,
        }), 200    

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        try: 
            actor.delete()

        except:
            abort(422)

        return jsonify({
            "success": True,
            "deleted": actor_id,
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if(body is None):
            abort(422)
        
        try:
            if 'title' in body:
                movie.title = body['title']
            if 'release_date' in body:
                movie.release_date = body['release_date']
            
            movie.update()
        
        except:
            abort(422)

        return jsonify({
            "success": True,
            "updated": movie_id,
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        
        body = request.get_json()
        if(body is None):
            abort(422)
        
        try:
            if 'name' in body:
                actor.name = body['name']
            if 'age' in body:
                actor.age = body['age']
            if 'gender' in body:
                actor.gender = body['gender']

            actor.update()

        except:
            abort(422)
        
        return jsonify({
            "success": True,
            "updated": actor_id,
        }), 200

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def notFound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['description']
        })
        response.status_code = ex.status_code
        return response
    
    return app