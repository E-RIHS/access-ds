# access-ds

*Access Documentation System* for documenting E-RIHS access projects.

## Installing and running *access-ds* in a development environment

### Prerequisites

* python >= 3.8
* docker
* docker-compose (optional)
* git (optional)

Note: this has only been tested on Linux boxes (Arch/Manjaro and Ubuntu)

### Get *access-ds* from github

Clone this github repository on your local machine (or download and unzip the package).

```shell
git clone https://github.com/E-RIHS/access-ds
cd access-ds
```

### Fetch and run MongoDB in a docker container

For fast development, a MongoDB docker-compose script is provided. Do not use this in a production environment (or at the very least, change the password!).

Launching this docker-compose script will automatically fetch the required docker containers and run them.

```shell
cd mongo_container
docker-compose up -d
cd ..
```

### Fetch all required Python packages

Different Python projects will require different Python packages. When you have multiple projects side-by-side, it could happen that these require different versions of the same packages, which could lead to issues. Therefore, it is good practice to run each project in a different *virtual environment*, each with its own set of dependencies.

First, create and activate a virtual environment:

```shell
python -m venv venv         # Creating a virtual environment for our application
source venv/bin/activate    # Activating the virtual environment
```

Secondly, install all required packages:

```shell
pip install -r requirements.txt  # Installing requirements
```

And finally, run the application using the Uvicorn web server:

```shell
cd src
uvicorn main:app --reload
```

## How to access *access-ds*

By default, Uvicorn will run as a local webserver on your computer on port 8000. 

At the moment, the user interface only has a single end-point: the project entry form:

```url
http://127.0.0.1:8000/project/new
```

The base URL for the RESTfull API:

```url
http://127.0.0.1:8000/api/
```

This API is documented using the OpenAPI (Swagger) specifications:

```url
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```