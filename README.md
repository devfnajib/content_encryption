# Content Management App
![Python](https://img.shields.io/badge/python-v3.11-blue.svg)

## Setup (in local)

1. Clone the repository on your local machine.

2. Create a file called **.env** in the root folder of the project, and add the parameters listed in **sample.env**. You will probably need your own credentials for **FLASK_APP**, **DB_HOST**, **DB_PORT**, **DB_NAME**, **DB_USERNAME** and
**DB_PASSWORD**.

3. Create a new environment with python 3.11 and activate it.

4. Install the packages listed in requirements.txt using the command **pip install -r requirements.txt**

5. Run following command to create DB Schema if you are running it for the first time and connecting with a clean DB.
     `flask db upgrade`

## Test the App

1. Run
     `pytest`

## Use the App

1. *Windows*: 
     In command line (CMD) window, run
     `Python start.py --port <port>`

2. You can also use Postman or other ways to send an HTTP requests to the server.