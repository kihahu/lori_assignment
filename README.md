# lori_assignment

## Description

This is a django application for managing renting of books:
* register
* obtain token
* rent a book
* view balance

The application can be accesed at https://loriassignment.herokuapp.com/
The documentation can be viewed at https://loriassignment.herokuapp.com/swagger


## Requirements
* Python 3.6
* postman
* pip
* virtualenv

# Installation
### 1)Clone the repo from GitHub:
$ git clone https://github.com/Ahmedsebit/lori_assignment.git

### 2) Create a virtual environment and install the necessary packages with:
$ virtualenv -p python3 env

### 3) Activate virtual environment:
$ source env/bin/activate

### 4) cd to the root of the api:
$ cd lori_assignment

### 5) Install requirements:
$ pip install -r requirements.txt

### 6) Make migrations:
$ python manage.py makemigrations

$ python manage.py migrate

# Runserver
$ python manage.py runserver

# Authentication
### Getting the token
The /api-token-auth/ is the authentication endpoint, which will be http://127.0.0.1:8000/api-token-auth/ from local server. The token is retrieved by submitting the username and password

### Using the token
The token is used in all the endpoints by adding the JWT+ token in the authorization header. Alternatively, the user can log in using the login links from the web application and the token will be generated, stored and refreshed by the application

# Accesing the application
The application can be accesed by using postman or for a better experience, using the web app.

# Users
Users include staff(superusers) and Normal Users
# Staff (superuser)
#### Are created using the command
$ python manage.py createsuperusers
#### Functions the supers users can do
| Funcion                                    | Request| command                 |
| ------------------------------------------ | -------| ------------------------|
| `/api-token-auth/`                         |`POST`  | Login and retrieve token|
| `/api/rest-auth/registration/`             |`POST`  | Registration            |
| `/api/<version>/book_rentals/`             |`GET`   | GET ALL RENTALS         |
| `/api/<version>/book_rentals/create`       |`POST`  | Create Book Rental      |
| `/api/<version>/book_rentals/users/balance/<user_id>`|`GET`   | GET balance   |
| `/api/<version>/books/`                    |`GET`   | GET All Books           |

# Running the tests
 $ python manage.py test --with-coverage
