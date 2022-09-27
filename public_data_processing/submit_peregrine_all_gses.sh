
#SBATCH --job-name=test245_samples
#SBATCH --output=/home/p283190/methylation_network/test_450kpipeline.out
#SBATCH --error=/home/p283190/methylation_network/test_450kpipeline.err

ftp_list="/data/p283190/GPL13534_series_ftplink.txt"
#ftp_list="/data/p283190/test.txt"
job_file="/home/p283190/methylation_network/scripts/get.sh"

while read uuid gse nr ftp ;
do
  echo ${gse} ${ftp}
  sbatch \
  --job-name ${gse} \
  --out /scratch/p283190/methylation/logs/${gse}.out \
  --error /scratch/p283190/methylation/logs/${gse}.err \
  ${job_file} ${gse} ${ftp}
done < ${ftp_list}

## quickly determine how many samples were collected
#unique_filepath="/scratch/p283190/methylation/unique_filepaths.txt"
#touch all_first_line.txt
#while read line; do
## reading each line
#echo $line
#head -1 $line >> all_first_line.txt
#done < $unique_filepath


#SBATCH --job-name=testGSE100386_normalization_steps
#SBATCH --output=/home/p283190/methylation_network/testGSE100386_normalization_steps.out
#SBATCH --error=/home/p283190/methylation_network/testGSE100386_normalization_steps.err

gse_list="/scratch/p283190/methylation/unique_gse_numbers.txt"
#gse_list="/scratch/p283190/methylation/test_gse_numbers.txt"
normalize_job_file="/home/p283190/methylation_network/scripts/normalize_merge.sh"

while read gse;
do
  echo ${gse}
  sbatch \
  --job-name ${gse}_normalize \
  --out /scratch/p283190/methylation/logs/${gse}_normalize.out \
  --error /scratch/p283190/methylation/logs/${gse}_normalize.err \
  ${normalize_job_file} ${gse}
done < ${gse_list}

#.ProbesWithZeroVarianceRemoved.QuantileNormalized.txt.gz
#.QuantileNormalized.txt.gz

#{'GSE89401', 'GSE100563', 'GSE89925', 'GSE77056', 'GSE94962',
#'GSE90015', 'GSE137830', 'GSE99996', 'GSE89400', 'GSE74797',
#'GSE138115', 'GSE100561', 'GSE94956'}
