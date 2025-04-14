To run the application with Docker, copy the project folder into
the folder with docker-compose.yml and call:

    docker-compose up --build


To run the application locally, create a virtual environment:

    python3 -m venv .venv

activate it

    . .venv/bin/activate

install Flask

    pip install flask

and, finally, run the application

    flask --app phil run