# API Challenge

## Description

An API challenge for servicepad interview, Hi Guys!

## Installation

1. Clone the repository: `git clone https://github.com/alexram1995/API_challenge.git`
2. Navigate to the project directory: `cd API_challenge`
3. Install the dependencies: `pip install -r requirements.txt`
4. Make sure you have 2 databases set up one to simulate "production" and other to "test" and add the host url in the `config.py` file.
5. The tables should be created by the code when you run it for the first time, you can run the next code in case those are not created 
```SQL
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE,
    password VARCHAR(80),
    fullname VARCHAR(80),
    photo VARCHAR(120)
);

CREATE TABLE publication (
    id INTEGER PRIMARY KEY,
    title VARCHAR(80),
    description TEXT,
    priority INTEGER,
    status VARCHAR(80),
    time_since_published INTERVAL,
    user_id INTEGER REFERENCES user(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE access_tokens (
    id INTEGER PRIMARY KEY,
    access_token TEXT,
    user_id INTEGER REFERENCES user(id)
);

## Running the API

1. Run the Flask development server: `flask run`
2. The API should now be accessible at `http://localhost:5000/`
3. You will have an admin account email='admin@example.com', password='password' with this you should be able to register other users
