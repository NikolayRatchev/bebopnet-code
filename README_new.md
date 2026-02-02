

conda env create -f environment.yml
conda activate bebopnet


On Windows, you may need:
KMP_DUPLICATE_LIB_OK=TRUE
due to OpenMP runtime duplication (NumPy / PyTorch).


Required Python packages:
- bidict==0.17.5
