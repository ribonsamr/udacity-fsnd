# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

### Tokens

- Manager: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjB6NjExQXBtbDQyXzR3TkctSm14TiJ9.eyJpc3MiOiJodHRwczovL3JpYi1mc25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhhNjViNjQ5ZjJmNDAwNjgzZWU2NjAiLCJhdWQiOiJjb2ZmZWVhcHAiLCJpYXQiOjE2MDI5MTkwOTksImV4cCI6MTYwMjkyNjI5OSwiYXpwIjoiVGNjQzVxYVNsV0xjaXZpS01WcUVpNTd5ZXZCR0lXRGMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.HZWQqdhOSbuBNZQTfzFcZ6O9XC0vaSACajEn57rqt70ZG_kPyla2t9DujERqX69epnINwcnabnZsmiLIoP2SaD0Z2tut4iSKhM7Nl5A77T6zTM9yFHSD2m45D3RFhl8LSaMR7ebN6NDfoJAjrbFQIRoIygqQNcEn-m7u_a7VZ8jC36vR2yOahYeAfOmwbhNQlW6a5_uQgKbv-S03EvQTVXAeU7AEs6DBDAcnj07aPsKuuQ7P-kOxzjArkZkhALMuO4ZSqz5KZoOm8QhCqIYWsZ7On_mgvgV8zKYvtBONtlMpI57lhQFkDWWcCA5EjwiheQ87G34Zva09f8TsE5i5TQ

- Barista: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjB6NjExQXBtbDQyXzR3TkctSm14TiJ9.eyJpc3MiOiJodHRwczovL3JpYi1mc25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjhhOTc3MGVhY2VjZDAwN2FkYzJjNDEiLCJhdWQiOiJjb2ZmZWVhcHAiLCJpYXQiOjE2MDI5MTkzMDQsImV4cCI6MTYwMjkyNjUwNCwiYXpwIjoiVGNjQzVxYVNsV0xjaXZpS01WcUVpNTd5ZXZCR0lXRGMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.fSmQmR78AKxyrW-a55RfVY89XIYmVJIn82PBdRA5ec7pjRByFeotNPHfay93cEZeYc_zdH8wEaYld_foHH-ZtD9YpS-y3L9MUKa1BJrVDflb0ekw7pSuG1zlNauH251ZA25tQKSqrJRSOYWFK0RYERGtDo6BUoFdQ6pWPCXmMoLod2oSNMB64JfLDWPiUPcbrsZROS2YJKxpseN7lFfM2JxUz9WB1Z3VCRhUMRQ8RAHexKWxCm-cOTTwAfTiMUrfc27_MWxfJToJMHh4wfiwXAbJVt3FNkN42N5VT8ZoA1xjm-5uFrvuMQEZ_ZuyI9X34pp1UQVWnK7-mnMJhZKIZw