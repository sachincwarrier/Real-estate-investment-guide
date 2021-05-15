# Real-estate-investment-guide
Real estate investment guide as part of Project for DVA course
## Description
This github page contains everything you need for implementing Redia. The frontend folder contains the HTML file and all the necessary code (e.g. css and image) in order to visualize the data. The API folder is the backend of the program which generates API calls for the program in order to communicate with the frontend. Lastly, redia folder contains all the data (except home sale data from Bridge API) needed to run the program and to generate the machine learning model. 

## Installation

### Home Sale Data (Optional):

The raw home sale data is available here. It is not required to run code, the data is already loaded in the database. The reading_json.py can read the raw data and load in into the database.

https://www.dropbox.com/s/8d3ai5gvcs36vlr/listings_coord.json?dl=0

It has over 110,000 records and over 200 fields.

### Clone the Github Repository (Optional)
Run the following command to clone the repository to your local machine. The code is attached in submission, so this is not required.

git clone https://github.gatech.edu/mjammu3/cse6242.git

### Running the code
Go to the root directory where the docker-compose.yml file is present  and run the following code.

### Bring up the containers and services
docker-compose up -d --force-recreate

go to http://localhost/ in the browser and you will be able to access the application

### Bring down the containers and services
docker-compose down --rmi all

## Execution
Redia is available at: http://ec2-52-20-232-151.compute-1.amazonaws.com/
