FROM continuumio/miniconda3

WORKDIR /discite

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "senior-design", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure fastapi is installed:"
RUN python -c "import fastapi"

# The code to run when container is started:
COPY app .

WORKDIR /discite/app

ENTRYPOINT ["uvicorn", "main:app"]
