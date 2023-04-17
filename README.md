# Casting Agency - Udacity Final Capstone Project Documentation 

## URL location for the hosted API:
The live API is accessible [here](http://localhost:5000/). 
The home route offers a template page with some information and login button but as its frontend has not built yet, it offer no other functionality. I use it to login to the Auth0 and get JWT for different roles. 

## Information about dependencies, local development and detailed instructions about scripts to set up authentication, install any project dependencies and run the development server.
To set up and start the backend server, we need to setup a Virtual Environment using virtualenv. After activating Virtual Environment, install the dependencies from 'Requirements.txt' using the following command.

`pip install -r requirements.txt`

After installation of the required dependancies, start the Flask App using following commands.

### For Windows CMD:
`set FLASK_APP=app`<br/>
`set FLASK_DEBUG=True`<br/>
`flask run`<br/>

### For Linux or Git:
`export FLASK_APP=app`<br/>
`export FLASK_ENV=development`<br/>
`flask run`<br/>

The application will be running on [localhost:5000](http://localhost:5000/). <br>

Note: All the secrets are stored in .env file.

### Postman collections
Two postman collections have been included in the files, one is for local testing and the other is for testing API on live server. 

The collections contains active JWT tokens for easily testing the API. 

The collections are stored in the root directory with following names and purposes.
1. Capstone_test_local
2. Capstone_test_live 

Moreover, the API has test_app.py file to test its endpoints. Three different active JWT tokens for three different roles have been hardcoded in the file for ease of testing. You can use the following commands to run it. 

`python test_app.py`<br/>


Note: Please run it once as on subsequent runs, the delete testcases may fail. You may change the ids of some test cases to test again.


## Documentation of API behavior and RBAC controls
The API entertains following three roles with different set of permissions.

### Roles and Permissions:
1. Casting Assistant
Has following permissions:
1. GET:Actors
2. GET:Movies

2. Casting Director
Has following permissions:
1. GET:Actors
2. GET:Movies
3. PATCH:Movies
4. PATCH:Actors
5. DELETE:Actors
6. POST:Actors

3. Executive Producer
Has all the permissions which are:
1. GET:Actors
2. GET:Movies
3. PATCH:Movies
4. PATCH:Actors
5. DELETE:Actors
6. DELETE:Movies
7. POST:Actors
8. POST:Movies


## API Endpoints
`GET /actors`<br/>
It will return the list of actors.

`GET /actors?page=${integer}`<br/>
It will return the actors on the given page.

`POST /actors/`<br/>
It will save the data in the database.

`PATCH /actors/${integer}`<br/>
It will update the provided actor.

`DELETE /actors/${integer}`<br/>
It will delete the provided actor.

`GET /movies`<br/>
It will return the list of movies.

`POST /movies`<br/>
It will post a new movie in the database.

`PATCH /movies/${integer}`<br/>
It will update the provided movie.

`DELETE /movies/${integer}`<br/>
It will return the list of actors.



