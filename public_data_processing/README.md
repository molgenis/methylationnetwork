This directory contains scripts for processing the public 450K data.

*get.sh*: downloads the idat files from GEO given the GSE number and ftp link

*normalize_merge.sh*: calculates m-values per project dataset and do normalization before concatenting with other project data

*merge_all_gse_files.py*, *qqnorm_merged_all_data.sh*: concatenate data from all processed projects

*methylation_data_examine.py*: removes outliers based on PC1 value

*peregrine_large_pca.py*: performs PCA with Cpgsite as the features
