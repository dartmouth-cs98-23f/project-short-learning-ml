FROM continuumio/miniconda3

WORKDIR /code

COPY ./environment.linux.yml /code/environment.yml

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "senior-design", "/bin/bash", "-c"]

RUN python -c "import fastapi"

COPY ./app /code/app

WORKDIR /code/app

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
