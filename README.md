# Travel companion

## Running the application

The application can be run using the following command: `docker-compose up`. 
It will run the tests, migrations and start the development server.
## Endpoints

The application has 3 main REST endpoints:

1. `/api/trips/`
    - GET -> returns all the trips in the app
    - POST -> adds a trip to the app
    - `{id}/` -> PUT/PATCH/DELETE - mutates existing trips, GET - retrieves trip details
    - `{id}/cities/` -> GET -> returns all the destinations in a trip
2. `/api/cities/`
    - GET -> returns all the available cities (destinations) in the app
    - POST -> adds a new city to the app
    - `{id}/` -> PUT/PATCH/DELETE - mutates existing cities, GET - retrieves all the city's details
3. `/api/users/`
    - GET -> returns all the users of the app
    - POST -> adds a new user
    - `{id}/` -> PUT/PATCH/DELETE - mutates existing users, GET - retrieves user details
    - `{id}/trips/` -> GET - retrieves the trips of a user
4. `/auth/`
    - POST -> the request body should contain the username and the password of a registered user
           -> returns the access token

For request body examples, please check the viewset tests.

