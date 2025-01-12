import os
import sys

from airflow.hooks import subprocess

if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
from airflow.decorators import dag, task
from constants.file_paths import FilePaths
import papermill as pm


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def publish():

    @task(task_id="start")
    def _dummy_start():
        pass

    @task(task_id="trigger_notebook")
    def _trigger_notebook():
        pm.execute_notebook(
            FilePaths.notebook_path,
            FilePaths.notebook_output_path,
            kernel_name="python3"
        )

    @task(task_id="host_notebook")
    def _host_notebook():
        # Host the executed notebook on localhost
        output_dir = os.path.dirname(FilePaths.notebook_output_path)
        subprocess.Popen(
            [
                "jupyter",
                "notebook",
                "--no-browser",
                "--ip=0.0.0.0",
                "--port=8888",
                "--NotebookApp.token=''",
                output_dir
            ],
        )

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    trigger_notebook = _trigger_notebook()
    host_notebook = _host_notebook()
    end = _dummy_end()

    start >> trigger_notebook >> host_notebook >> end


publish()
