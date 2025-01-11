# Project for INSA Lyon course Data Engineering IF5OT7

in progress...

## Instructions for running the project

#### 0. Prerequisites

Copy the `.env.template` file to `.env` and fill in the necessary environment variables.

#### 1. Download the FBI crime data

1. Go to https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
2. Scroll to section "Crime Incident-Based Data by State"
3. Select "California" and "2023" and click "Download"
4. A "CA" folder should have been downloaded, move that to ./data directory
5. You should have the following structure:

```
data
└── CA
    ├── agencies.csv
    ├── NIBRS_ACTIVITY_TYPE.csv
    ├── ...
├── ...
├── dags
├── file_readers
└── handlers
```

#### 2. Start the project

```bash
make start
```

- Creates a docker container with the project's dependencies.
- Starts an airflow server at `http://localhost:8080/`, along with a postgres database.

Go to the url to view the available DAGs and run them.

Username and password for airflow are defined in the `.env` file.

#### 3. Copy dependencies from the container for local development

```bash
make copy-dependencies
```

This copies the container dependencies to the ./local_dependencies directory.

This makes autocomplete and other stuff work with the dependencies while developing locally.

#### 4. Stop the project

```bash
make stop
```

When done, run this to stop and remove all the project's docker containers.
