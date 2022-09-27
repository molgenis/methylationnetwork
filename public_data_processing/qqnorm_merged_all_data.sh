#!/usr/bin/env bash
#SBATCH --time=4:00:00
#SBATCH --partition=himem
#SBATCH --cpus-per-task=2
#SBATCH --mem=200gb
#SBATCH --nodes=1
#SBATCH --get-user-env=L
#SBATCH --job-name=qqnorm
#SBATCH --output=/scratch/p283190/methylation/logs/qqnorm.out
#SBATCH --error=/scratch/p283190/methylation/logs/qqnorm.err

ml Java
# qqnorm the merged files
jar_file=/home/p283190/methylation_network/eqtl-mapping-pipeline-1.4.7-SNAPSHOT/eqtl-mapping-pipeline.jar
traitfile=/data/p283190/methylation/complete_public_450_values.dupGSMDeleted.QuantileNormalized.dat
outdir=/scratch/p283190/methylation/
logFile=/data/p283190/methylation/qqnorm_public_450_values.log

java -Xmx200g -Xms200g -jar ${jar_file} \
--mode normalize \
--in ${traitfile} \
--out ${outdir} \
--centerscale | tee ${logFile}
