# Project for INSA Lyon course Data Engineering IF5OT7

in progress...

## Instructions for running the project

#### 0. Prerequisites

Copy the `.env.template` file to `.env` and fill in the necessary environment variables.

Ask one of the project owners for the `FBI_API_KEY`.

#### 1. Start the project

```bash
make start
```

- Creates a docker container with the project's dependencies.
- Starts an airflow server at `http://localhost:8080/`.

Go to the url to view the available DAGs and run them.

Username and password for airflow are defined in the `.env` file.

##### 1.1. Running the pipelines

The project contains three pipelines:

1. `ingest` - Ingests data from the FBI API and stores them in temporary files
2. `transform` - Cleans and transforms the data from the temporary files and stores them in a MongoDB database
3. `publish` - Loads the data from the MongoDB database to a Jupyter notebook, which creates plots and tables to analyze the data

##### 1.2. Viewing the results

After running all the pipelines, the `publish` pipeline has created a Jupyter notebook with the results. You can view the notebook at `http://localhost:8888/`. Select the notebook `notebook-prod.ipynb` to view the results.

#### 2. Copy dependencies from the container for local development

```bash
make copy-dependencies
```

This copies the container dependencies to the ./local_dependencies directory.

This makes autocomplete and other stuff work with the dependencies while developing locally.

#### 3. Stop the project

```bash
make stop
```

When done, run this to stop and remove all the project's docker containers.
