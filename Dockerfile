FROM python:3.10-slim-bullseye

RUN echo "### --- Ubuntu dependencies --- ###" &&\
    apt-get update && \
    apt-get install -y \
    g++ \
    cmake \
    unzip \
    curl \
    poppler-utils \
    && echo "### --- Directory setup --- ###"

WORKDIR /app

COPY ./app .

# PACKAGES 
RUN pip install --no-cache-dir -r requirements_d.txt

# Command to run the application because this will 
CMD ["uvicorn", "endpoint:app", "--reload", \
    "--host", "0.0.0.0" ,\
    "--port", "80"]

EXPOSE 80