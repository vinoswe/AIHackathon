# Synthetic Data Generation and Sandbox

# DataSynthesizer

DataSynthesizer generates synthetic data that simulates a given dataset.

> It aims to facilitate the collaborations between data scientists and owners of sensitive data. It applies Differential Privacy techniques to achieve strong privacy guarantee.



## Table of contents
* [Approach](#approach)
* [Setup & Prerequisites](#setup)
* [Usage](#usage)
* [Model](#model)
* [Reference](#Reference)


## Approach
Used latest version of Python by using Bayesian Networks Model and DataSynthesizer, pandas & numpy packages for creating sythentic data and retoolapi.dev for sandbox environment and mock api creation from synthetic dataset(DataSynthesizer).

## Setup
Please follow one of the below steps: 

**Prerequisites**

We can use the ```owndata.csv``` input file to feed the dataset to the program

 **POC Environment Setup**

### Install DataSynthesizer

```bash
Download python (Goto https://www.python.org/downloads/) and install.
pip install DataSynthesizer
pip install pandas
pip install numpy
```

**Running the Python**

```bash
Open the pythen runner then run the 'DataSynthesizer.py' file or
goto cmd promt then enter python DataSynthesizer.py
```
Finally you will get ```sythetic_data.csv``` file with syhthetic data.

**Sandbox**

We are using ```retoolapi.dev``` online environment for sanbox enviornment. We have to upload ```sythetic_data.csv``` dataset files in this site to generate the mock api with endpoint.
```
Endpoint https://retoolapi.dev/142yCB/employees
HTTP methods : GET, URI : /142yCB/employees
```

Once the endpoint is up, please use the postman collection collection

## Usage

##### Assumptions for the Input Dataset

1. The input dataset is a table in first normal form.
2. When implementing differential privacy, DataSynthesizer injects noises into the statistics within **active domain** that are the values presented in the table.

## Model

A Bayesian network could be used to create multiple synthetic data sets that are then released by an official statistics agency while the original data remain confidential.

## Reference

>
> For more details, please refer to [DataSynthesizer: Privacy-Preserving Synthetic Datasets](doc/cr-datasynthesizer-privacy.pdf)
