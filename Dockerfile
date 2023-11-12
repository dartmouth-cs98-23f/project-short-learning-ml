FROM continuumio/miniconda3

WORKDIR /code

COPY ./environment.linux.yml /code/environment.yml

# RUN apt-get update && apt-get install -y build-essential

ENV DEBIAN_FRONTEND noninteractive

RUN apt update
RUN apt install -y 'libgl1-mesa-dev'
RUN apt install -y 'ffmpeg' 'libsm6' 'libxext6'

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "senior-design", "/bin/bash", "-c"]

RUN python -c "import fastapi"

COPY ./app /code/app

# WORKDIR /code

ENTRYPOINT [ "conda" , "run", "-n", "senior-design", "--no-capture-output", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
