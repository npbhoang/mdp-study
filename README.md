# Models Trump Code: An Empirical Analysis of GDPR Compliance

***Authors: Hoang Nguyen, Srdan Krstic, and David Basin***

Artifacts developers: 
- Hoang Nguyen (hoang.nguyen@inf.ethz.ch) 
- Srdan Krstic (srdan.krstic@inf.ethz.ch)

> **Evaluation.** Badges awarded: **Available**, **Evaluated (Functional)**, but **not Reproduced**.

This artifact repository contains the materials used in the graduate-level security engineering course described in the paper. These materials include:
- (i) Exercise and lab assignments designed to introduce students to the &nu;ActionGUI tool and the Python/Flask framework.
- (ii) Project description and implementation templates for the Event Platform, covering both the &nu;ActionGUI and Python/Flask, together with the master solutions and a representative subset of the evaluation test cases. The post-study questionnaire is also included.

The provided materials support independent inspection and replication of the course setup and project tasks described in the paper. **Due to data protection restrictions, we cannot share the complete test set as well as the participant data collected during the study.**

## Repository Structure

The repository is organized into two top-level components: the six-week [`course_materials`](course_materials) training phase and the [`course_project`](course_project) Event Platform. Training and course projects are distributed as self-contained, dockerized applications with their own `README.md`.

### Training materials (`course_materials`)

The exercises and lab assignments are organized into one folder per week, each with a `materials/` subfolder (the lab handout `labX.pdf` accompanied by the starter/template projects given to students) and a `solutions/` subfolder (the corresponding reference solutions).

<pre>
course_materials
├── <a href="course_materials/Week1">Week1</a>/
│   ├── materials/
│   │   ├── <a href="course_materials/Week1/materials/lab1.pdf">lab1.pdf</a> — lab 1 handout (Flask basics)
│   │   ├── <a href="course_materials/Week1/materials/thoughts-template.zip">thoughts-template.zip</a> — Thoughts app starter template
│   │   └── <a href="course_materials/Week1/materials/miniapp-template.zip">miniapp-template.zip</a> — minimal Flask tutorial starter template
│   └── solutions/
│       └── <a href="course_materials/Week1/solutions/thoughts-simple.zip">thoughts-simple.zip</a> — Thoughts app starter implementation
├── <a href="course_materials/Week2">Week2</a>/
│   ├── materials/
│   │   ├── <a href="course_materials/Week2/materials/lab2.pdf">lab2.pdf</a> — lab 2 handout (data persistence &amp; authentication)
│   │   ├── <a href="course_materials/Week2/materials/minisql-template.zip">minisql-template.zip</a> — SQL exercise starter
│   │   └── <a href="course_materials/Week2/materials/minisql.zip">minisql.zip</a> — SQL exercise examples
│   └── solutions/
│       ├── <a href="course_materials/Week2/solutions/thoughts-sql.zip">thoughts-sql.zip</a> — Flask-SQLAlchemy persistence
│       ├── <a href="course_materials/Week2/solutions/thoughts-user.zip">thoughts-user.zip</a> — Flask-User authentication
│       └── <a href="course_materials/Week2/solutions/thoughts-sec-base.zip">thoughts-sec-base.zip</a> — Week 2 end state (persistence + auth); baseline carried into Week 3
├── <a href="course_materials/Week3">Week3</a>/
│   ├── materials/
│   │   ├── <a href="course_materials/Week3/materials/lab3.pdf">lab3.pdf</a> — lab 3 handout (access control &amp; privacy)
│   │   ├── <a href="course_materials/Week3/materials/thoughts-sec-template.zip">thoughts-sec-template.zip</a> — Week 3 starter: the baseline plus access-control scaffolding to complete
│   │   ├── <a href="course_materials/Week3/materials/thoughts-sec-flaskuser.zip">thoughts-sec-flaskuser.zip</a> — Role-based Access Control via Flask-User
│   │   ├── <a href="course_materials/Week3/materials/thoughts-confidentiality-template.zip">thoughts-confidentiality-template.zip</a> — data confidentiality starter implementation
│   │   └── <a href="course_materials/Week3/materials/thoughts-privacy-template.zip">thoughts-privacy-template.zip</a> — privacy starter implementation
│   └── solutions/
│       ├── <a href="course_materials/Week3/solutions/thoughts-sec-manual.zip">thoughts-sec-manual.zip</a> — role-based access control (manual checks)
│       ├── <a href="course_materials/Week3/solutions/thoughts-confidentiality.zip">thoughts-confidentiality.zip</a> — data confidentiality enforcement
│       └── <a href="course_materials/Week3/solutions/thoughts-privacy.zip">thoughts-privacy.zip</a> — privacy policy: purposes and consent
├── <a href="course_materials/Week4">Week4</a>/
│   ├── materials/
│   │   ├── <a href="course_materials/Week4/materials/lab4.pdf">lab4.pdf</a> — lab 4 handout (OCL)
│   │   └── <a href="course_materials/Week4/materials/ocl-test.zip">ocl-test.zip</a> — OCL exercise starter
│   └── solutions/
│       └── <a href="course_materials/Week4/solutions/ocl-solution.zip">ocl-solution.zip</a> — OCL exercise solutions
└── <a href="course_materials/Week5-6">Week5-6</a>/
    ├── materials/
    │   ├── <a href="course_materials/Week5-6/materials/lab5-6.pdf">lab5-6.pdf</a> — lab 5-6 handout (&nu;ActionGUI)
    │   └── <a href="course_materials/Week5-6/materials/thoughts-nag-template.zip">thoughts-nag-template.zip</a> — &nu;ActionGUI starter implementation and base models
    └── solutions/
        └── <a href="course_materials/Week5-6/solutions/thoughts-nag.zip">thoughts-nag.zip</a> — Thoughts generated with &nu;ActionGUI with refined models
</pre>

The table below (based on **Table 4, Appendix A** of the paper) summarizes the concepts covered each week:

| Week | Materials | Concepts | Folder (lab handout) |
|:----:|-----------|----------|----------------------|
| 1 | Flask basics | Routing, request handling, Jinja templates, and the in-memory Thoughts application | [`Week1`](course_materials/Week1) ([`lab1.pdf`](course_materials/Week1/materials/lab1.pdf)) |
| 2 | Flask basics | Data persistence with Flask-SQLAlchemy and authentication with Flask-User | [`Week2`](course_materials/Week2) ([`lab2.pdf`](course_materials/Week2/materials/lab2.pdf)) |
| 3 | Flask security & privacy | Role-based access control using Flask-User and manual checks, data confidentiality, and privacy policy declaration and enforcement for purposes and consent | [`Week3`](course_materials/Week3) ([`lab3.pdf`](course_materials/Week3/materials/lab3.pdf)) |
| 4 | OCL | Object Constraint Language (OCL) | [`Week4`](course_materials/Week4) ([`lab4.pdf`](course_materials/Week4/materials/lab4.pdf)) |
| 5 | &nu;ActionGUI | Data and security modeling | [`Week5-6`](course_materials/Week5-6) ([`lab5-6.pdf`](course_materials/Week5-6/materials/lab5-6.pdf)) |
| 6 | &nu;ActionGUI | Privacy modeling | [`Week5-6`](course_materials/Week5-6) |

### Event Platform project (`course_project`)

The artifacts related to the Event Platform project are organized by phase (`Development`, `Evolution`) and tool (Flask, &nu;ActionGUI).

<pre>
course_project
├── <a href="course_project/description">description</a>/ — natural-language project descriptions
│   ├── <a href="course_project/description/Development.pdf">Development.pdf</a> — Development phase description
│   └── <a href="course_project/description/Evolution.pdf">Evolution.pdf</a> — Evolution phase description
├── <a href="course_project/templates">templates</a>/ — incomplete starter implementations
│   ├── <a href="course_project/templates/Development">Development</a>/
│   │   ├── <a href="course_project/templates/Development/Flask">Flask</a>/ — Flask starter implementation
│   │   └── <a href="course_project/templates/Development/NuActionGUI">NuActionGUI</a>/ — &nu;ActionGUI starter (data/security/privacy base models)
│   └── <a href="course_project/templates/Evolution">Evolution</a>/
│       ├── <a href="course_project/templates/Evolution/Flask">Flask</a>/ — Flask starter implementation with Evolution updates
│       └── <a href="course_project/templates/Evolution/NuActionGUI">NuActionGUI</a>/ — &nu;ActionGUI starter models, extended with Evolution updates
├── <a href="course_project/solutions">solutions</a>/ — master solutions
│   ├── <a href="course_project/solutions/Development">Development</a>/
│   │   ├── <a href="course_project/solutions/Development/Flask/project.py">Flask/project.py</a> — the Flask implementation solution
│   │   └── <a href="course_project/solutions/Development/NuActionGUI/project.ptm">NuActionGUI/project.ptm</a> — the &nu;ActionGUI privacy model solution
│   └── <a href="course_project/solutions/Evolution">Evolution</a>/
│       ├── <a href="course_project/solutions/Evolution/Flask/project.py">Flask/project.py</a> — the Flask implementation solution
│       └── <a href="course_project/solutions/Evolution/NuActionGUI/project.ptm">NuActionGUI/project.ptm</a> — the &nu;ActionGUI privacy model solution
├── <a href="course_project/tests">tests</a>/ — privacy tests (representative subset; see note below) and testing environments
│   ├── <a href="course_project/tests/test_driver.py">test_driver.py</a> — evaluation driver
│   ├── <a href="course_project/tests/docker">docker</a>/ — dockerized evaluation harness
│   ├── <a href="course_project/tests/testcases">testcases</a>/ — collection of privacy testcases
│   │   ├── <a href="course_project/tests/testcases/Development">Development</a>/
│   │   │   ├── <a href="course_project/tests/testcases/Development/Flask">Flask</a>/ — privacy testcases, grouped by category: {none, basic, complex}
│   │   │   └── <a href="course_project/tests/testcases/Development/NuActionGUI">NuActionGUI</a>/ — privacy testcases, grouped by category: {none, basic, complex}
│   │   └── <a href="course_project/tests/testcases/Evolution">Evolution</a>/
│   │       ├── <a href="course_project/tests/testcases/Evolution/Flask">Flask</a>/ — privacy testcases, grouped by category: {none, basic, complex}
│   │       └── <a href="course_project/tests/testcases/Evolution/NuActionGUI">NuActionGUI</a>/ — privacy testcases, grouped by category: {none, basic, complex}
│   └── <a href="course_project/tests/environments">environments</a>/ — testing environments
│       ├── <a href="course_project/tests/environments/Development">Development</a>/
│       │   ├── <a href="course_project/tests/environments/Development/Flask">Flask</a>/ — runnable Flask app for testing
│       │   └── <a href="course_project/tests/environments/Development/NuActionGUI">NuActionGUI</a>/ — &nu;ActionGUI models + generated project used for testing
│       └── <a href="course_project/tests/environments/Evolution">Evolution</a>/
│           ├── <a href="course_project/tests/environments/Evolution/Flask">Flask</a>/ — runnable Flask app for testing
│           └── <a href="course_project/tests/environments/Evolution/NuActionGUI">NuActionGUI</a>/ — &nu;ActionGUI models + generated project used for testing
└── <a href="course_project/survey/Questionnaire.md">survey/Questionnaire.md</a> — post-study questionnaire
</pre>

## Installation and Usage

### Requirements
Because the tools are dockerized, Docker is the only required dependency. The artifact was tested with **Docker version 29.5.3** and **Docker Compose version v5.1.4**. Recent versions of Docker and Docker Compose are expected to work as well.

> **Note on build times.** The first `docker compose up --build` can take several minutes because Docker must pull the base image and install dependencies. The &nu;ActionGUI labs may take longer because they also set up Java/ANTLR. *Subsequent* builds reuse Docker's cache and typically start within a few seconds.

### Running the Training Labs
Each weekly lab is described in its `labX.pdf` handout. The starter and solution projects under `course_materials` are distributed as self-contained zip archives. To run a project, unzip the desired archive and follow the instructions in the corresponding `README.md`.

> **Note: Lab materials are intentionally incomplete.** The `*-template` lab projects are *starters* that students are expected to complete. Some endpoints return HTTP 500 by design until the corresponding security or privacy logic is implemented. These lab projects are nevertheless expected to build and start successfully.

### Running the Templates
This applies to the four Event Platform implementation templates under [`course_project/templates`](course_project/templates): Flask and &nu;ActionGUI, for both the Development and Evolution phases. Each template is a self-contained, dockerized application. The quick-start commands are listed below, while the full instructions are provided in the corresponding template's `README.md`. Run the commands from the relevant template directory.

**Flask** (READMEs: [Development](course_project/templates/Development/Flask/README.md), [Evolution](course_project/templates/Evolution/Flask/README.md))

```bash
# build (first run) and start, then visit http://localhost:5000
docker compose up
# stop the container
docker compose stop
```

The functional code you complete lives in `EventPlatformFlask/src/project.py`.

**&nu;ActionGUI** (READMEs: [Development](course_project/templates/Development/NuActionGUI/README.md), [Evolution](course_project/templates/Evolution/NuActionGUI/README.md))

```bash
# build and start the `nag-app` container
docker compose up --build -d
# open a shell inside the container, then run the following commands in it
docker exec -it nag-app bash
# set up the Python virtual environment
cd /app/src && python3 -m venv .venv && . .venv/bin/activate && pip3 install -r requirements.txt
# (re)generate the enforced app from the models
python3 generate.py -p EventPlatformNAG -o project -re
# start the app, then visit http://localhost:5000
cd /app/project/EventPlatformNAG && flask --app app.py run --host=0.0.0.0
# stop the container
docker compose stop
```

The data/security/privacy models you complete live in `models/EventPlatformNAG/`.

> **Note: Template codebases are intentionally incomplete.**
Because the baseline templates implement only functional behavior and do not yet enforce security or privacy policies, requests that would normally be guarded by such enforcement may surface errors. For example, an unauthenticated user opening `/profile` returns HTTP 500 because the naive implementation reads the current user's data without first checking whether a user is logged in.

### Running the Tests

> **Note: only a representative subset of the privacy tests is published here.** To preserve the integrity of the test suite for **future iterations of the course**, this artifact ships only a few test cases per subpart (three where available) rather than the complete grading suite used in the study; the full suite is withheld. The published tests are a strict subset of the originals, so the master solutions still pass every test included here.

The privacy testcases under [`course_project/tests`](course_project/tests) are organized by phase (`Development`, `Evolution`) and tool (Flask, &nu;ActionGUI), and within each into three variants under `privacy/`, each split into `part1`, `part2`, … subparts. The three variants correspond to the privacy categories evaluated in the paper:

- **`none`** — no consent is recorded, so every access to personal data must be denied.
- **`basic`** — consent is granted for exactly the basic purpose an action uses, so the access is allowed.
- **`complex`** — consent is granted for a complex purpose in the purpose hierarchy that subsumes the action's basic purpose, so the access is allowed.

See the paper for the precise definitions of these categories.

> **Note on the evaluation driver.** The test driver ([`course_project/tests/test_driver.py`](course_project/tests/test_driver.py)) was written and tested with the assistance of Claude (Anthropic).

**Running with Docker.** To avoid installing Python and the codegen dependencies on the host, a dockerized harness is provided under [`course_project/tests/docker`](course_project/tests/docker) (see its [`README`](course_project/tests/docker/README.md)). Build the image once, then pass the driver's arguments after the service name:

```bash
cd course_project/tests/docker
docker compose build

# e.g. the nuactiongui master solution runs
docker compose run --rm tests --phase dev --tech nag --solution
docker compose run --rm tests --phase evol --tech nag --solution

# e.g. the flask master solution runs
docker compose run --rm tests --phase dev --tech flask --solution
docker compose run --rm tests --phase evol --tech flask --solution
```

Omitting `--solution` runs against the template instead of the master solution. 

Add `--category <none|basic|complex>` or `--part <partN>` to narrow a run. 

## License

This artifact is released under the MIT License; see [`LICENSE`](LICENSE).