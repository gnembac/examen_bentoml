# Admissions Prediction Service

A simple MLOps project built with BentoML. The project trains a machine learning model to predict admission chances and exposes it as a local HTTP API.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Training Workflow](#training-workflow)
- [Docker Workflow](#docker-workflow)
- [API Usage](#api-usage)
- [Testing](#testing)
- [Notes](#notes)
- [License](#license)

## Overview

This repository contains a small BentoML service for an admissions prediction use case. It includes data preparation, model training, API serving, containerization, and automated tests. BentoML is used to package the service and build a Docker image for deployment.

## Features

- Data preparation script.
- Model training script.
- BentoML service with `/login` and `/predict`.
- JWT-based authentication.
- Pytest test suite.
- Docker image export for submission.

## Project Structure

```text
.
├── bentofile.yaml
├── requirements.txt
├── README.md
├── data/
│   └── processed/
├── src/
│   ├── prepare_data.py
│   ├── train_model.py
│   └── service.py
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_login.py
    └── test_predict.py
```

## Requirements

- Python 3.12
- Docker
- A virtual environment named `.venv`
- Dependencies from `requirements.txt`

## Setup

```bash
# VM Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Training Workflow

### 1) Prepare the data

```bash
# VM Bash
python src/prepare_data.py
```

### 2) Train the model

```bash
# VM Bash
python src/train_model.py
```
After training, the model is saved in the BentoML Model Store.

## Docker Workflow

### 1) Build the Bento

```bash
# VM Bash
bentoml build
```

### 2) Containerize the Bento

```bash
# VM Bash
bentoml containerize admission_prediction_service:latest
```

### 3) Save the Docker image

```bash
# VM Bash
docker save admission_prediction_service:latest -o admission_prediction_service.tar
```

### 4) Load the Docker image

```bash
# VM Bash
docker load -i admission_prediction_service.tar
```

### 5) Run the service

```bash
# VM Bash
docker run --rm -p 3000:3000 admission_prediction_service:latest
```

The API will be available at `http://127.0.0.1:3000`. Docker loads images from tar archives with `docker load`, and `docker run` starts the container on the mapped port.

## API Usage

### Login

```bash
# VM Bash
curl -X POST http://127.0.0.1:3000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Predict

```bash
# VM Bash
curl -X POST http://127.0.0.1:3000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "GRE Score": 320,
    "TOEFL Score": 110,
    "University Rating": 4,
    "SOP": 4.5,
    "LOR": 4.0,
    "CGPA": 8.8,
    "Research": 1
  }'
```

## Testing

### Run all tests

```bash
# VM Bash
pytest -v
```

### Run only the tests folder

```bash
# VM Bash
pytest tests -v
```

Pytest automatically discovers test files such as `test_*.py`, and `-v` gives a more detailed output.


## License

This project is used for educational purposes in the DataScientest MLOps exam.