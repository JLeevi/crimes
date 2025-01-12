FROM apache/airflow:2.7.1

RUN pip install pymongo==4.10.1 papermill==2.4.0 notebook jupyter ipykernel matplotlib pandas seaborn
RUN python -m ipykernel install --user
