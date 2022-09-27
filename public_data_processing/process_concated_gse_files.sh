python merge_all_gse_files.py # merge all normalized files from all GSE projects
bash qqnorm_merged_all_data.sh # normalize the merged file
python methylation_data_examine.py # remove outliers based on the 1st PC, 3 standard deviation
bash peregrine_submit_pca.sh # perform PCA with Cpgsites as features
#python peregrine_large_pca.py
