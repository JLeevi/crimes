# Project for INSA Lyon course Data Engineering IF5OT7

This project examines the impact of a government-sanctioned Purge taking place in California. Using real-time data on crime patterns, offenders, and victims, we analyze the effects on society to highlight how such an event would alter communities and individual safety.

## Project Anlysis Questions

We aim to answer the following questions:

- What are the crimes people are most likely to commit based on their relationship with the victims?
- What are the most damaging types of crimes financially based on properties involved?
- How much do one's race, religion, and other characteristics put them at risk of being targeted?

## Instructions for Running the Project

### Prerequisites

1. Copy the `.env.template` file to `.env` and fill in the necessary environment variables.
2. Ask one of the project owners for the `FBI_API_KEY`.

**Data Sources**:
- CSV files: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
- FBI Crime Data API: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi

### Starting the Project

To start the project, run:

```bash
make start
```

This command:
- Creates a Docker container with the project's dependencies.
- Starts an Airflow server at http://localhost:8080/.

Go to the URL to view the available DAGs and run them. The username and password for Airflow are defined in the `.env` file.

### Running the Pipelines

The project contains three pipelines:

1. **Ingest**: Retrieves data from CSV files and FBI API, storing it in temporary files. (Ingestion Pipeline)
2. **Transform**: Cleans and transforms the data, storing it in a MongoDB database. (Staging/Wrangling Pipeline)
3. **Publish**: Loads data from MongoDB to a Jupyter notebook for analysis and visualization. (Production Pipeline)

### Viewing the Results

After running all pipelines, access the Jupyter notebook at http://localhost:8888/. Select `notebook-prod.ipynb` to view the results.

### Local Development

To copy dependencies from the container for local development, run:


```bash
make copy-dependencies
```

This copies the container dependencies to the `./local_dependencies` directory, enabling autocomplete and other features while developing locally.

### Stopping the Project

To stop and remove all project Docker containers, run:


```bash
make stop
```

## Pipeline Details

### 1. Ingest Pipeline

- Fetches data from CSV files and FBI API
- Stores raw data in temporary files
- Handles errors such as API timeouts and rate limiting

### 2. Transform Pipeline (Staging/Wrangling)

- Cleans data (fixes inconsistencies, missing values, etc.)
- Transforms data for analysis
- Validates data against schema definitions
- Stores cleaned data in MongoDB

### 3. Publish Pipeline (Production)

- Retrieves data from MongoDB
- Analyzes data using Pandas, NumPy, or SciPy
- Creates visualizations with Matplotlib
- Generates insights and summaries in a Jupyter notebook

### :hammer_and_wrench: Used Technologies for the project :

<div>
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/de/AirflowLogo.png" title="Airflow" alt="Airflow" width="100" height="40"/>&nbsp;
  <img src="https://github.com/marwin1991/profile-technology-icons/blob/main/icons/docker.png" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  <img src="https://github.com/marwin1991/profile-technology-icons/blob/main/icons/mongodb.png" title="MongoDB" alt="MongoDB" width="40" height="40"/>&nbsp;
  <img src="https://github.com/marwin1991/profile-technology-icons/blob/main/icons/redis.png" title="Redis" alt="Redis" width="40" height="40"/>&nbsp;
  <img src="https://github.com/marwin1991/profile-technology-icons/blob/main/icons/pandas.png" title="Pandas" alt="Pandas" width="40" height="40"/>&nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Jupyter_logo.svg" title="Jupyter Notebook" alt="Jupyter Notebook" width="40" height="40"/>
</div>
