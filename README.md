# AIHackathon
Synthetic Data generation and Sandbox

DataSynthesizer

DataSynthesizer generates synthetic data that simulates a given dataset.

It aims to facilitate the collaborations between data scientists and owners of sensitive data. It applies Differential Privacy techniques to achieve strong privacy guarantee.

For more details, please refer to DataSynthesizer: Privacy-Preserving Synthetic Datasets

Install DataSynthesizer
pip install DataSynthesizer
Usage
Assumptions for the Input Dataset
The input dataset is a table in first normal form (1NF).
When implementing differential privacy, DataSynthesizer injects noises into the statistics within active domain that are the values presented in the table.
Use Jupyter Notebook
After installing DataSynthesizer and Jupyter Notebook, open and try the demos in ./notebooks/

DataSynthesizer__random_mode.ipynb
DataSynthesizer__independent_attribute_mode.ipynb
DataSynthesizer__correlated_attribute_mode.ipynb
Use Web UI
The dataResponsiblyUI is a Django project that includes DataSynthesizer. Please follow the steps in Run the Web UIs locally and run DataSynthesizer by visiting http://127.0.0.1:8000/synthesizer in a browser.
