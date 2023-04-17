from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from auth.auth import requires_auth, AuthError
from models import setup_db, Actor, Movie
from flask_cors import CORS
import os
from jose import jwt


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_AUDIENCE = os.getenv('API_AUDIENCE')
AUTH_CLIENT_ID = os.getenv('AUTH_CLIENT_ID')


RESULTS_PER_PAGE = 10

# App configuration


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # routes
    @app.route('/')
    def index():
        login_uri = 'https://{}/authorize?audience={}&response_type=token&client_id={}&redirect_uri={}'.format(
            AUTH0_DOMAIN, API_AUDIENCE, AUTH_CLIENT_ID, 'http://localhost:5000/')
        
        return render_template('index.html', login_url = login_uri)


    # Pagination of restuls

    def paginate_results(request, data):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RESULTS_PER_PAGE
        end = start + RESULTS_PER_PAGE

        actors = [actor.format() for actor in data]
        paginated_results = actors[start:end]

        return paginated_results

    # routes
    # TODO: get_actors : DONE

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            paginated_actors = paginate_results(request, actors)
            if actors:
                return jsonify({
                    'success': True,
                    'actors': paginated_actors,
                    'total_actors': len(actors)
                })
            else:
                return jsonify({
                    'success': True,
                    'message': 'no actor found'
                })
        except Exception as e:
            print(e)
            abort(422)

    # TODO: post_actors : Done
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)
        
        try:
            if body is not None:
                actor = Actor(
                    name=name,
                    gender=gender,
                    age=age,
                    movie_id=movie_id)
                actor.insert()

                return jsonify({
                    'success': True,
                    'created': actor.id
                })
        except Exception as e:
            print(e)
            abort(422)

    # TODO: delete_actors : Done
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        print(actor)
        
        try:    
            actor.delete()
            return jsonify({
                    'success': True,
                    'deleted': actor_id
                })
                
        except Exception as e:
            print(e)
            if actor is None:
                abort(404)
            abort(422)

    # TODO: patch_actors : Done
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.movie_id = movie_id
            actor.update()

            return jsonify({
                'success': True,
                'updated': actor.id
            })

        except Exception as e:
            print(e)
            if actor is None:
                abort(404)
            abort(422)

    # routes
    # TODO: get_movies : DONE
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            paginated_movies = paginate_results(request, movies)
            
            if movies:
                return jsonify({
                    'success': True,
                    'movies': paginated_movies,
                    'total_movies': len(movies)
                })
            else:
                return jsonify({
                    'success': True,
                    'message': 'no movies found',
                    'total_movies': len(movies)
                })
                
        except Exception as e:
            print(e)
            abort(422)

    # TODO: post_movies : DONE

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        body = request.get_json()
        title = body.get('title', None)
        release = body.get('release_date', None)
        try:
            if body is not None:
                movie = Movie(title=title, release_date=release)
                movie.insert()
                return jsonify({
                    'success': True,
                    'created': movie.id
                })

        except Exception as e:
            print(e)
            abort(422)

    # TODO: delete_movies : DONE

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        print(movie)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id
            })

        except Exception as e:
            print(e)
            if movie is None:
                abort(404)
            abort(422)

    # TODO: patch_movies : Done
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):

        body = request.get_json()
        title = body.get('title', None)
        release = body.get('release_date', None)

        try:
            if body is not None:
                movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
                movie.title = title
                movie.release_date = release

                movie.update()

                return jsonify({
                    'success': True,
                    'updated': movie.id
                })

        except Exception as e:
            print(e)
            if movie is None:
                abort(404)
            abort(422)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'unauthorized'
        }), 401

    @app.errorhandler(AuthError)
    def notAuthenticatedUser(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error
        }), auth_error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
