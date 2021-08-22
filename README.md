# Full Stack Nanodegree Capstone Project

## Casting Agency Application

The Casting Agency is a company that is responsible for creating movies and managing and assigning actors to those movies. This application allows users to interact with the database of actors and movies, in three different ways (depending on role permission level):

1. Casting Assistant: Can view actors and movies
2. Casting Director: Can view actors and movies, add or delete an actor from the database, and modify actors or movies
3. Executive Producer: As above, and can add or delete a movie from the database

## Using the application

The application is hosted on Heroku, at the address https://capstone-cameron-barker.herokuapp.com. Users can interact with the application using a tool such as cURL or Postman, and the below endpoints.

To obtain the JWT required for role-based access, users must login at https://capstone-cameron-barker.herokuapp.com/login. The accounts are:
- Casting Assistant: assistant@cameroncasting.com
- Casting Director: director@cameroncasting.com
- Executive Producer: producer@cameroncasting.com
The password for these accounts will be provided in the submission comments for the project.

### Endpoints

```js
GET '/movies'
- Fetches the set of movies on the database
- Request Arguments: None
- Minimum permission required: Casting Assistant
- Returns: A success message and status, an object of movies, and the total number of categories.
{
    'success': True,
    'status': 200,
    'movies': [
        {
            'id': 1,
            'title': 'Avengers: Endgame',
            'release': 'Thursday, 25 Apr 2019'
        }
    ],
    'total_movies': 100
}
```

```js
GET '/actors'
- Fetches the set of actors on the database
- Request Arguments: None
- Minimum permission required: Casting Assistant
- Returns: A success message and status, an object of actors, and the total number of actors.
{
    'success': True,
    'status': 200,
    'actors': [
        {
            'id': 1,
            'name': 'Chris Hemsworth',
            'age': 38,
            'gender': 'M'
        }
    ],
    'total_movies': 100
}
```

```js
DELETE '/movies/${id}'
- Deletes a specified movie using the id of the movie
- Request Arguments: id - integer
- Minimum permission required: Executive Producer
- Returns: A success message and status, the id of the deleted movie, an object with the remaining movies, and the new total number of movies
{
    'success': true,
    'status': 200,
    'deleted': 15,
    'movies': [
        {
            'id': 1,
            'title': 'Avengers: Endgame',
            'release': 'Thursday, 25 Apr 2019'
        }
    ],
    'total_movies': 99
}
```

```js
DELETE '/actors/${id}'
- Deletes a specified actor using the id of the actor
- Request Arguments: id - integer
- Minimum permission required: Casting Director
- Returns: A success message and status, the id of the deleted actor, an object with the remaining actors, and the new total number of actors
{
    'success': true,
    'status': 200,
    'deleted': 15,
    'movies': [
        {
            'id': 1,
            'name': 'Chris Hemsworth',
            'age': 38,
            'gender': 'M'
        }
    ],
    'total_actors': 99
}
```

```js
POST '/movies'
- Sends a post request in order to add a new movie to the database
- Request Body: 
{
    'title':  'Captain Marvel',
    'release':  '08/03/2019'
}
    - Note: Release date must be of the form 'DD/MM/YYYY'
- Minimum permission required: Executive Producer
- Returns: a success message and status, the id of the new movie, an object with the list of movies, and the new total number of movies
{
    'success': true,
    'status': 200,
    'created': 150,
    'movies': [
        {
            'id': 1,
            'title': 'Avengers: Endgame',
            'release': 'Thursday, 25 Apr 2019'
        }
    ],
    'total_movies': 101
}
```

```js
POST '/actors'
- Sends a post request in order to add a new actor to the database
- Request Body: 
{
    'name':  'Brie Larson',
    'age':  31,
    'gender': 'F'
}
    - Note: Gender is a single character ('M'(ale)/'F'(emale)/'O'(ther))
- Minimum permission required: Casting Director
- Returns: a success message and status, the id of the new actor, an object with the list of actors, and the new total number of actors
{
    'success': true,
    'status': 200,
    'created': 150,
    'actors': [
        {
            'id': 1,
            'name': 'Chris Hemsworth',
            'age': 38,
            'gender': 'M'
        }
    ],
    'total_actors': 101
}
```

```js
PATCH '/movies/${id}'
- Sends a patch request in order to update the movie with the specified id in the database
- Request Body: 
{
    'title':  'Captain Marvel',
    'release':  '08/03/2019'
}
    - Note: Release date must be of the form 'DD/MM/YYYY'
- Minimum permission required: Casting Director
- Returns: a success message and status, and an object with the updated movie details
{
    'success': true,
    'status': 200,
    'updated_movie': [
        {
            'id': 1,
            'title': 'Captain Marvel',
            'release': '08/03/2019'
        }
    ]
}
```

```js
PATCH '/actors/${id}'
- Sends a patch request in order to update the actor with the specified id in the database
- Request Body: 
{
    'name':  'Brie Larson',
    'age':  31,
    'gender': 'F'
}
    - Note: Gender is a single character ('M'(ale)/'F'(emale)/'O'(ther))
- Minimum permission required: Casting Director
- Returns: a success message and status, and an object with the updated actor details
{
    'success': true,
    'status': 200,
    'updated_actor': [
        {
            'id': 1,
            'name': 'Brie Larson',
            'age': 31,
            'gender': 'F'
        }
    ]
}
```

### Error Handling

Errors are returned as JSON objects in the following format:
```js
{
    'success': false,
    'error': 404,
    'message': 'resource not found'
}
```
The API will return five error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal server error

## Testing

The endpoint test scripts are stored in test_app.py, and use a connection to a local PostgreSQL database called agency_test, which can be populated using the test_database.psql file. To setup the database and perform the tests, run the following commands: 
```
dropdb agency_test
createdb agency_test
psql agency_test < test_database.psql
python test_app.py
```
Note that these tests also require setup of environment variables, which can be done by running `source setup.sh`.

RBAC testing can be performed using the casting-agency Postman collection. Please note that the JWTs will expire at approximately 09:30 UK time on Monday 23rd August.