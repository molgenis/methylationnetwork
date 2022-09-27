#!/usr/bin/env bash
#SBATCH --time=15:00:00
#SBATCH --mem=500gb
#SBATCH --cpus-per-task=1
#SBATCH --partition=himem
#SBATCH --job-name=pcaOnCpgsites
#SBATCH --output=/scratch/p283190/methylation/logs/pcaOnSamples.out
#SBATCH --error=/scratch/p283190/methylation/logs/pcaOnSamples.err


ml Python/3.7.4-GCCcore-8.3.0
ml scikit-learn/0.21.3-foss-2019b-Python-3.7.4
#ml matplotlib

python /home/p283190/methylation_network/scripts/peregrine_large_pca.py \
--npy_path /scratch/p283190/methylation/complete_public_450_values.dupGSMDeleted.QuantileNormalized.ProbesCentered.SamplesZTransformed.npy \
--perform_pca 1 \
--n_components 500 \
--pca_path /scratch/p283190/methylation/merged_mval/pca_onCpgs_centerScaled.pkl \
--eigenVectors12_figpath /scratch/p283190/methylation/merged_mval/eigVec_pcaOnCpgsites_centerScaledData.png

#
#python /home/p283190/methylation_network/scripts/peregrine_large_pca.py \
#--npy_path /scratch/p283190/methylation/merged_mval/unique_public_450_values.QuantileNormalized.3STDoutlierDeleted.ProbesCentered.SamplesZTransformed.npy \
#--perform_pca 1 \
#--n_components 100 \
#--pca_path /scratch/p283190/methylation/merged_mval/pca_centerScaled.pkl \
#--mean_std_perRow_fig_path /scratch/p283190/methylation/merged_mval/mean_std_perCpg_centerScaledData.png \
#--mean_std_perCol_fig_path /scratch/p283190/methylation/merged_mval/mean_std_perSample_centerScaledData.png \
#--row_name Cpgsite \
#--col_name Individual \
#--eigenVectors12_figpath /scratch/p283190/methylation/merged_mval/eigVec_centerScaledData.png
