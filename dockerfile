# Use official Jupyter PySpark notebook base image
FROM jupyter/pyspark-notebook:latest

# Switch to root to install packages
USER root

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install jupyter && \
    pip install --no-cache-dir pyspark && \
    pip install --no-cache-dir -r requirements.txt


# Replace this block in your Dockerfile
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

# And make sure JAVA_HOME is set
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH




# Create base logs and rejected folders (but NOT the conversion_log subfolder!)
RUN mkdir -p /app/logs && \
    mkdir -p /app/rejected && \
    chmod -R 777 /app/logs /app/rejected

#  copy the jars/ folder into the container:
COPY jars /app/jars

# Copy all project files into container
COPY . .

# Switch back to notebook user
USER $NB_UID

# Run PySpark ETL
# CMD ["spark-submit", "--jars", "/app/jars/mssql-jdbc-12.10.1.jre11.jar", "etl_pipeline.py"]
CMD ["start-notebook.sh", "--NotebookApp.token=''"]
