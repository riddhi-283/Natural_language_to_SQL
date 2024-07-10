# Natural_language_to_SQL
This repository contains a code file written in Python to build a web application for converting natural language query to a SQL query using LLM calls. The sql query will then be performed on the database and th query results will be displayed on screen in tabular format for better clarity and understanding. Additionally, there is a "Download results as csv" button which will allow the users to download the obtained query results in form of a csv. The application is deployed in the form of a simple website built using HTML, CSS and JavaScript for frontend and uses Python-Flask at backend. The LLM used is google-gemini-pro model.

<br>

## Screenshots
![Screenshot 2024-07-10 163730](https://github.com/riddhi-283/Natural_language_to_SQL/assets/124153277/ef5eff1c-9b8d-4b49-9729-41fc9452abde)
![Screenshot 2024-07-10 163755](https://github.com/riddhi-283/Natural_language_to_SQL/assets/124153277/85c1e5cf-9d91-4d3e-8ffb-f82ce674077d)

<br>

# Installation
To run this project in your laptop:
```sh
git clone git@github.com:riddhi-283/Natural_language_to_SQL.git
```

# Setting-up the application

### Creating Database
Open Mysql Workbench in your local machines and create a database "atliq_tshirts" using the sql code file provided.
Make sure that the MySQL server is running on your laptop while running this application.

### Setting up LLM model
Get your free google-api key from "makersuite.google.com"
<br> 
Create a .env file and paste your google api key.
```sh
GOOGLE_API_KEY=''
```

### Running the application
```sh
pip install -r requirements.txt
python app.py
```


<br>
