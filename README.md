# Project for INSA Lyon course Data Engineering IF5OT7

in progress...

---

Currently, the main data exploration work is in the `main.ipynb` notebook.

### Download the data

**To use the current notebook, you need to download the FBI crime data**:

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
└── main.ipynb
```

---

## Instructions for running the project

### Start the project

```bash
make start
```

Starts an airflow server at `http://localhost:8080/`, along with a postgres database.

### Copy dependencies from the container for local development

```bash
make copy-dependencies
```

This copies the container dependencies to the ./local_dependencies directory.

This makes autocomplete and other stuff work with the dependencies while developing locally.

### Stop the project

```bash
make stop
```

stops and removes all the project's docker containers.
