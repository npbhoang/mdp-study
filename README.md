# Models Trump Code: An Empirical Analysis of Enforcing GDPR Compliance

***Authors: Anonymous Author(s)***

Artifacts developer(s): Anonymous

This repository contains the materials used throughout the graduate security engineering course.
This includes:
- (i) Exercise and lab assignments designed to introduce students to 𝜈ActionGUI tool and Python/Flask framework.
- (ii) Descriptions and templates of the Event Platform project written in 𝜈ActionGUI tool and Python/Flask framework.

Due to ethical concerns, personal data related to the study will not be disclosed.
Nevertheless, interested readers are welcome to use the provided artifacts for their own research.

## Repository Structure

* `course_materials` contains artifacts related to (i).
  - `NuActionGUI` contains two key artifacts for 𝜈ActionGUI:
    - `labs` provides a tutorial and installation guide for the 𝜈ActionGUI tool. The tutorial is in the `tutorial` sub-directory and a Docker setup for running the 𝜈ActionGUI tool is in the `NuActionGUI.zip` archive.
    - `assignments` contains an exercise assignment for 𝜈ActionGUI. In this assignment, students are tasked with implementing security policies for a simple Thoughts application using the 𝜈ActionGUI tool. A description of the application can be found in the `assignment.pdf`, and the base implementation (i.e., implementation without security policies defined and enforced) is located in the `messageBoardInit` sub-directory.
  - `Flask\labs` includes three tutorials for Flask: `tutorial1`, `tutorial2`, and `tutorial3`, along the docker setup for running Python/Flask application in `installation` sub-directory.
* `course_project` contains artifacts related to (ii).
  - `project_description` contains files that describe the project and its evolution in natural language.
  - `project_templates` contains the 𝜈ActionGUI and Flask implementation templates.
    - `TemplateFlask` contains the code template for Flask in the Development phases.
    - `TemplateNAG` contains the code template for 𝜈ActionGUI in the Development phases.
    - `TemplateUpdates` contains the code template updates for Flask and 𝜈ActionGUI in the Evolution phase.

Instructions for compiling and running the application can be found in the `README.md` of the corresponding folders.

## Installation and Usage

### Requirements
Since these tools are dockerized, to have Docker installed is the minimum requirements.
