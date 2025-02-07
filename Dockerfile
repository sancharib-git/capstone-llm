FROM public.ecr.aws/dataminded/spark-k8s-glue:v3.5.2-hadoop-3.3.6-v1

USER 0
ENV PYSPARK_PYTHON python3
WORKDIR /opt/spark/work-dir

#TODO add your project code and dependencies to the image
COPY . /opt/spark/work-dir
RUN pip install uv
RUN uv sync
RUN uv pip install -e .
RUN pip install -r requirements.txt
CMD python3 src/capstonellm/tasks/clean_json.py



