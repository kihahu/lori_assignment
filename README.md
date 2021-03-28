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

# Deployment To AWS
This service can be deployed to aws to run as a containerized application on aws EKS service with fargate nodes to run the workloads. Deployment is achieved using terraform (version 0.14.8). This is automated to be part of the CI/CD pipeline by making use of github actions.

## Infrastructure
Opensource terraform modules have been used to create the infrastructure for the application, namely:
- https://github.com/Harshetjain666/terraform-aws-eks-fargate-cluster.git
- github.com/azavea/terraform-aws-postgresql-rds
Below modifications have been carried out to meet the task of deploying the loribooks application:
- Subnet lookup for use with kubernetes ingress and service annotations to allow the ALB targets to detect pods in all subnets:
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L1-L12
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L118
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L146
- Container specification for deployment
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L55-L61
- Application secret to store username and password
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L14-L26
- Read application configs as environment variables:
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L63-L96
- Create db subnet group to be used with postgres module
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/vpc/main.tf#L120-L127
- Create sns needed by postgres module
    -- https://github.com/kihahu/lori_assignment/blob/main/terraform/vpc/main.tf#L129-L131
## Pull Requests
On making a PR, a github action runs and builds the docker image for the application, a terraform init, validate and plan are also perfomed. Any errors in docker build or the terraform code will result in the github action failing.

## Merge To Main
On a PR being approved and merged to main, a github action runs to build the docker image and push it to aws ECR, a release tag of the latest code is created, terraform init and apply are then carried  out deploying the application as container using aws fargate for  on demand nodes.

Notes:
- The initial CI/CD run builds out all the infrastructure i.e
    - vpc and subnets
    - alb
    - eks cluster
    - postgres database
this initial run might take a long time, but subsequent imporovement changes and deploys should be fast.
- Each PR needs to bump up the release version otherwise the on merge job will fail due to conflict with existing release tag.


## Known Bugs
- The ALB (application loadbalancer) only gets deployed in the public subnets despite attempts to disable auto subnet discovery by removing this tags https://github.com/kihahu/lori_assignment/blob/main/terraform/vpc/main.tf#L23 https://github.com/kihahu/lori_assignment/blob/main/terraform/vpc/main.tf#L41 in the subnets and adding the subnets annotation to the kubernetes (eks) ingress and service objects see https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L117-L120 https://github.com/kihahu/lori_assignment/blob/main/terraform/kubernetes/app.tf#L146 . As such, a manual change needs to be applied should the infrastructure be recreated from scratch to the ALB to obtain targets from all available subnets.
- ALB targets register as unhealthy due to returned status of 400 on calling the 8000:/ endpoint, this seems related to the Django config for allowed hosts https://github.com/kihahu/lori_assignment/blob/main/lori_assignment/settings.py#L27, the application still gets served on the url b69ee518-fargatenode-lorib-be0e-1165705763.us-east-1.elb.amazonaws.com since ALB passes traffic to the pods.
- makemigrations migrate and runserver have been combined into one script i.e entrypoint.sh, initial plan was to have the three seperated out, with makemigrations and migrate run as init containers and runserver as the main container in the pod. But migrate fails on subsequent runs and as such the init container would fail, if the error from migrate were to be addressed, the init container design should be implemented.

## Improvements
- Include application testing to the i.e run the command `python manage.py test --with-coverage` by creating a custom docker container github action see https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action 