# INSTRUCTIONS ON HOW TO EXECUTE THE APP

We have 2 ways of using the app: Executing the back-end and the front-end separately or running each corresponding Docker images by means of the docker-compose file.
#### IMPORTANT: The back-end runs in `localhost:8000` while the front-end runs in `localhost:3000` (for both options)

### OPTION 1: Running the back-end and the front-end separately

#### Back-end

1) Install the dependencies

`pip install -r requirements.txt`

2) Execute the API in the folder which the API is located (backend/)

`uvicorn main:app`

#### Front-end

1) Install the dependencies

`npm install`

2) Execute the front-end inside its folder (frontend/app)

`npm start`

### OPTION 2: Running it by means of Docker compose

1) Run in the root of the project:

`docker-compose up --build`

## TESTS

To run the tests of the back-end, you need to go to the tests folder:

`cd backend/tests`

And run:

`pytest`


