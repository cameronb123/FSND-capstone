import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def home():
    return "Welcome to the Casting Agency app"

  # GET endpoints
  # Movies
  @app.route('/movies', methods=['GET'])
  def get_movies():
    #Query the database
    movies = Movie.query.order_by(Movie.id).all()
    movie_list = [movie.format() for movie in movies]

    if len(movies) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'movies': movie_list,
      'total_movies': len(movies)
    })

  # Actors
  @app.route('/actors', methods=['GET'])
  def get_actors():
    #Query the database
    actors = Actor.query.order_by(Actor.id).all()
    actor_list = [actor.format() for actor in actors]

    if len(actors) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'movies': actor_list,
      'total_movies': len(actors)
    })

  # DELETE endpoints

  
  # Error handlers
  # 404
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed'
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable entity'
      }), 422

  @app.errorhandler(500)
  def internal_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'internal server error'
      }), 500

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)