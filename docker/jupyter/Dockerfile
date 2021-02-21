FROM jupyter/datascience-notebook

USER root

RUN apt-get update && \ 
    apt-get install -y fonts-ipafont fonts-ipaexfont

# User change
USER jovyan

# Install python modules
COPY ./app/jupyter/requirements.txt requirements.txt
RUN pip install -r requirements.txt