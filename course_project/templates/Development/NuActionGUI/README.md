# README

This is a dockerized version of the **NuActionGUI (AG)** framework. From data, security, and
privacy models it generates a Flask web application with built-in runtime enforcement of the
specified security and privacy requirements.

## Build and start the container

With Docker installed, build the image and start the container:

```
docker compose up --build -d
```

This starts a container named `nag-app`. The local `NuActionGUI/` folder is mounted at `/app`
inside the container, so files created there are visible on both the host and the container.
Open a shell in the container with:

```
docker exec -it nag-app bash
```

Use `docker compose stop` / `docker compose start` to stop and restart it, and
`docker compose down` to remove it.

The `/app/project/EventPlatformNAG` directory contains the EventPlatformNAG application
implemented naively: there is no privacy policy and all actions are allowed (`fullAccess`)
for all roles. (Some functionality may break because `VISITOR` is not an actual user.)

Your task is to define the security and privacy model in `/app/models/EventPlatformNAG`
according to the provided project description.

## Regenerate the security and privacy enforcement

Inside the container, set up a virtual environment in `/app/src`:

```
cd /app/src
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

Then (re)compile the models and generate the enforced application:

```
python3 generate.py -p EventPlatformNAG -o project -re
```

(When regenerating, you may first need to delete the existing database at
`/app/project/EventPlatformNAG/instance/`.)

## Run the application

From inside the virtual environment, start the generated app:

```
cd /app/project/EventPlatformNAG
flask --app app.py run --host=0.0.0.0
```

The application is then reachable at http://localhost:5000.
