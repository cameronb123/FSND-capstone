import os
import datetime
from flask import Flask, json, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def home():
    return "Welcome to the Casting Agency app"
  
  @app.route('/login')
  def login_redirect():
    return redirect('''
      https://cameronb123.eu.auth0.com/authorize?audience=agency
      &response_type=token
      &client_id=bxqMoDrnTsGjbqY3a4UUx3uefsw3ccgU
      &redirect_uri=https://capstone-cameron-barker.herokuapp.com/
    ''')

  # GET endpoints
  # Movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):
    #Query the database
    movies = Movie.query.order_by(Movie.id).all()
    movie_list = [movie.format() for movie in movies]

    if len(movies) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'status': 200,
      'movies': movie_list,
      'total_movies': len(movies)
    })

  # Actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    #Query the database
    actors = Actor.query.order_by(Actor.id).all()
    actor_list = [actor.format() for actor in actors]

    if len(actors) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'status': 200,
      'actors': actor_list,
      'total_actors': len(actors)
    })

  # DELETE endpoints
  # Movies
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(movie_id, jwt):
    # Check if movie exists in database
    movie = Movie.query\
      .filter(Movie.id == movie_id).one_or_none()

    if movie:
      try:
        # Delete the movie, return the new list of movies
        movie.delete()
        movies = Movie.query.order_by(Movie.id).all()
        movie_list = [movie.format() for movie in movies]

        return jsonify({
          'success': True,
          'status': 200,
          'deleted_id': movie_id,
          'movies': movie_list,
          'total_movies': len(movies)
        })
      except:
        # Handle error in processing deletion
        abort(422)
    else:
      # No movie matches movie id
      abort(404)

  # Actors
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(actor_id, jwt):
    # Check if actor exists in database
    actor = Actor.query\
      .filter(Actor.id == actor_id).one_or_none()

    if actor:
      try:
        # Delete the actor, return the new list of actors
        actor.delete()
        actors = Actor.query.order_by(Actor.id).all()
        actor_list = [actor.format() for actor in actors]

        return jsonify({
          'success': True,
          'status': 200,
          'deleted_id': actor_id,
          'actors': actor_list,
          'total_actors': len(actors)
        })
      except:
        # Handle error in processing deletion
        abort(422)
    else:
      # No actor matches actor id
      abort(404)

  # POST endpoints
  # Movies
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(jwt):
    body = request.get_json()
    # Handle error if request is empty
    if body == {}:
      abort(400)
    
    # Get details of new movie from the request
    new_title = body.get('title', None)
    new_release = body.get('release', None)
    try:
      release_datetime = datetime.datetime.strptime(new_release, "%d/%m/%Y")
      new_release = release_datetime.date()
    except:
      abort(400)

    try:
      # Create new movie and insert into db
      movie = Movie(title=new_title, release=new_release)
      movie.insert()

      # Return success message with created movie id
      movies = Movie.query.order_by(Movie.id).all()
      movie_list = [movie.format() for movie in movies]

      return jsonify({
        'success': True,
        'status': 200,
        'created_movie': movie.id,
        'movies': movie_list,
        'total_movies': len(movies)
      })
    except:
      abort(422)

  # Actors
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(jwt):
    body = request.get_json()
    # Handle error if request is empty
    if body == {}:
      abort(400)
    
    # Get details of new actor from the request
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    try:
      # Create new actor and insert into db
      actor = Actor(name=new_name,
                    age=new_age,
                    gender=new_gender)
      actor.insert()

      # Return success message with created actor id
      actors = Actor.query.order_by(Actor.id).all()
      actor_list = [actor.format() for actor in actors]

      return jsonify({
        'success': True,
        'status': 200,
        'created_actor': actor.id,
        'actors': actor_list,
        'total_actors': len(actors)
      })
    except:
      abort(422)
  
  # PATCH endpoints
  # Movies
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(movie_id, jwt):
    # Get movie from database
    movie = Movie.query\
      .filter(Movie.id == movie_id).one_or_none()

    if movie:
      body = request.get_json()
      if body == {}:
        abort(400)

      # Get updated details from request
      new_title = body.get('title', None)
      new_release = body.get('release', None)
      
      # Set new details to movie
      if new_title:
        movie.title = new_title
      if new_release:
        try:
          release_datetime = datetime.datetime.strptime(new_release, "%d/%m/%Y")
          new_release = release_datetime.date()
        except:
          abort(400)
        movie.release = new_release
      
      try:
        movie.update()

        # Return success message
        return jsonify({
          'success': True,
          'status': 200,
          'updated_movie': movie.format()
        })
      except:
        abort(422)
    else:
      # Movie doesn't exist in database
      abort(404)

  # Actors
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(actor_id, jwt):
    # Get actor from database
    actor = Actor.query\
      .filter(Actor.id == actor_id).one_or_none()

    if actor:
      body = request.get_json()
      if body == {}:
        abort(400)

      # Get updated details from request
      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)
      # Set new details to actor
      if new_name:
        actor.name = new_name
      if new_age:
        actor.age = new_age
      if new_gender:
        actor.gender = new_gender
      
      try:
        actor.update()

        # Return success message
        return jsonify({
          'success': True,
          'status': 200,
          'updated_actor': actor.format()
        })
      except:
        abort(422)
    else:
      # Actor doesn't exist in database
      abort(404)
  
  # Error handlers
  # 404
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'status': 400,
          'message': 'bad request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'status': 404,
          'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          'success': False,
          'status': 405,
          'message': 'method not allowed'
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'status': 422,
          'message': 'unprocessable entity'
      }), 422

  @app.errorhandler(500)
  def internal_error(error):
      return jsonify({
          'success': False,
          'status': 500,
          'message': 'internal server error'
      }), 500
    
  @app.errorhandler(AuthError)
  def auth_error(error):
      print(error)
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error
      }), error.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)