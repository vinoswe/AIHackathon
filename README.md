# Synthetic Data Generation and Sandbox

# DataSynthesizer

DataSynthesizer generates synthetic data that simulates a given dataset.

> It aims to facilitate the collaborations between data scientists and owners of sensitive data. It applies Differential Privacy techniques to achieve strong privacy guarantee.
>
> For more details, please refer to [DataSynthesizer: Privacy-Preserving Synthetic Datasets](doc/cr-datasynthesizer-privacy.pdf)



### Usage

##### Assumptions for the Input Dataset

1. The input dataset is a table in first normal form ([1NF](https://en.wikipedia.org/wiki/First_normal_form)).
2. When implementing differential privacy, DataSynthesizer injects noises into the statistics within **active domain** that are the values presented in the table.


## Table of contents
* [Approach](#approach)
* [Setup & Prerequisites](#setup)
* [API Specifications](#api-specifications)
* [Build Pipeline](#build-pipeline)
* [Sonar Analysis](#sonar-analysis)


## Approach
Used latest version of Python by using Bayesian Networks Model and DataSynthesizer, pandas & numpy packages for creating sythentic data and retoolapi.dev for sandbox environment from synthetic dataset from the DataSynthesizer.

## Setup
Please follow one of the below steps: 

**Prerequisites**

We can use the ```owndata.csv``` input file to feed the dataset to the program

 **POC Environment Setup**

### Install DataSynthesizer

```bash
pip install DataSynthesizer
pip install pandas
pip install numpy
```

**Running the Python**

```bash
python DataSynthesizer.py
```
Finally you will get ```sythetic_data.csv``` file with syhthetic data.

**Sandbox**

We are using ```retoolapi.dev``` online environment for sanbox enviornment. We have to upload ```sythetic_data.csv``` dataset files in this site to generate the mock api to test


**Testing the APIs**
Once the endpoint is up, please use the postman collection collection, `bookstore-api.postman_collection.json` available on root directory to validate the APIs
 

The same is also upload here [Postman Collection](https://www.getpostman.com/collections/a6e3b49a39bae0d29b71)

## API Specifications
Followed API first design by implementing Swagger specifications. Please refer the bookstore-swagger.yaml at the root directory. 

Alternatively, the same specifications can be viewed on [SwaggerHub](https://app.swaggerhub.com/apis/sharafnu/bookstore/1.0.0)

## Build Pipeline
Integrated using Github Actions. The below stages are incorporated -
* Unit Tests
* Code Quality Check using SonarCloud
* Publish Artificats to GitHub packages
* Build and publish docker images to public repo

![Github Actions Workflow](./screenshots/gihub-actions.png)

## Sonar Analysis
Integrated the pipeline with SonardCloud as part of CI. 

Latest report can be seen by accessing the below URL

[View SonarCloud Dashboard](https://sonarcloud.io/dashboard?id=sharafnu_bookstore-api)

![Sonar Cloud Dashboard](./screenshots/sonar-dashboard.png)
