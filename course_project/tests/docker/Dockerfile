# Dockerized test harness for the Event Platform evaluation suite.
#
# Wraps tests/test_driver.py so reviewers can run the pytest corpus without
# installing Python, pip dependencies, or the NuActionGUI codegen toolchain
# on the host. The ANTLR parsers are shipped pre-generated as Python, so no
# Java/ANTLR is needed at runtime -- only the pure-Python requirements below.
#
# Build context is the course_project/ directory (see docker-compose.yml).
FROM python:3.11-slim

# build-essential is needed to compile the forbiddenfruit C extension.
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /artifact

# Install Python deps first so the layer caches across source changes.
# The NuActionGUI and Flask environments share the same Flask/SQLAlchemy/User
# stack; installing both requirements files makes the image self-sufficient for
# every suite -- `--tech nag` and `--tech flask`, Development and Evolution.
COPY tests/environments/Development/NuActionGUI/src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY tests/environments/Development/Flask/requirements.txt /tmp/flask-requirements.txt
RUN pip install --no-cache-dir -r /tmp/flask-requirements.txt

# Copy the artifact (tests/, solutions/, templates/ are all referenced by
# test_driver.py). Runtime cruft is excluded via Dockerfile.dockerignore.
COPY . /artifact

WORKDIR /artifact/tests

# Forward all `docker run`/`docker compose run` arguments to test_driver.py,
# e.g.  docker compose run --rm tests --phase dev --tech nag --solution
ENTRYPOINT ["python", "test_driver.py"]
CMD ["--list"]
