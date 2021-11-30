# Instructions
This repository contain notebooks for the Manuscript: Integration of public DNA methylation and expression networks via eQTMs improves prediction of functional gene–gene associations.

## Requirements
Python 3.6.5 or above <br />
Python Packages listed in `Requirements.txt`

## Notebooks
#### eQTM_prediction_models.ipynb
This notebook contain python scripts for using the two models predicting 1) whether there is a eQTM effect between a CpG site and a nearby gene and 2) whether this eQTM association is a positive association or a negative one. 
#### tissue_disease_prediction_model.ipynb
This notebook contain python scripts for using the tissue prediction model based on the PC components from the MethylationNetwork. 
#### train_cca_for_public_datasets.ipynb
This notebook contain python scripts for using and training the CCA models and its corresponding preprocessing steps.
#### predict_genepairs_in_string.ipynb
This notebook contain python scripts for using and training models to predict whether there is a potential functional / physical associations between two genes.  
