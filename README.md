# Content Management App
![Python](https://img.shields.io/badge/python-v3.11-blue.svg)

## Setup (in local)

1. Clone the repository on your local machine.

2. Create a file called **.env** in the root folder of the project, and add the parameters listed in **sample.env**. You will probably need your own credentials for **DB_HOST**, **DB_PORT**, **DB_USERNAME** and
**DB_PASSWORD**.

3. Create a new environment with python 3.11 and activate it.

4. Install the packages listed in requirements.txt using the command **pip install -r requirements.txt**

## Use the new App

1. *Windows*: 
     In command line (CMD) window, run
     `flask run --port <port>`

2. Once the Flask server is running, you can use client.py to send a request. Please make sure that the port specified in **client.py** is the same where app is running.

3. You can also use Postman or other ways to send an HTTP requests to the server.