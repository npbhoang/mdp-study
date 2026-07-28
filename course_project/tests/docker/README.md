# Dockerized test harness

Run the Event Platform evaluation suite ([`../test_driver.py`](../test_driver.py))
inside a container, with no host setup beyond Docker. The image bundles Python,
the pinned pip dependencies, and the NuActionGUI codegen toolchain (the ANTLR
parsers ship pre-generated as Python, so no Java is required).

> **Note.** Only a representative subset of the privacy tests ships in this
> artifact (a few cases per subpart); the full grading suite is withheld for
> future iterations of the course. The master solutions still pass every
> published test.

## Build

```bash
cd course_project/tests/docker
docker compose build
```

## Run

Anything after the service name is passed straight to `test_driver.py`:

```bash
# NuActionGUI privacy suite against the master solution (expected: 100% pass)
docker compose run --rm tests --phase dev  --tech nag --solution
docker compose run --rm tests --phase evol --tech nag --solution

# ... against the (incomplete) template (expected: partial pass)
docker compose run --rm tests --phase dev  --tech nag
docker compose run --rm tests --phase evol --tech nag

# A single variant or part
docker compose run --rm tests --phase dev --tech nag --category complex
docker compose run --rm tests --phase dev --tech nag --category complex --part part5

# List every available phase/tech/category/part, or show all options
docker compose run --rm tests --list
docker compose run --rm tests --help
```

The runs are ephemeral: each invocation regenerates the application from the
models inside the container and leaves the host tree untouched. See the
[top-level README](../../../README.md#running-the-tests) for approximate
execution times.

## Without Compose

```bash
# Build (context must be course_project/)
docker build -f tests/docker/Dockerfile -t nag-tests course_project

# Run
docker run --rm -t nag-tests --phase dev --tech nag --solution
```
