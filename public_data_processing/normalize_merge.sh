#!/usr/bin/env bash
#SBATCH --time=2:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=50gb
#SBATCH --nodes=1
#SBATCH --get-user-env=L


gse_number=$1
# test
#gse_number="GSE100386"

#GSM2679976_6229009015_R03C01, GSM2679976_6229009015_R03C01
#cg00000769, cg00000622
source_dir=/scratch/p283190/methylation
code_dir=/home/p283190/methylation_network/scripts
output_450_dir=${source_dir}/output_450
mval_dir=${source_dir}/mval

mkdir -p ${mval_dir}

# merge the red and gree type1 files
ml Python
python ${code_dir}/merge_actions.py --gse "${gse_number}" --action "merge_green_red"

# ================================= Q-norm =====================================
ml Java
jar_file=/home/p283190/methylation_network/eqtl-mapping-pipeline-1.4.7-SNAPSHOT/eqtl-mapping-pipeline.jar

# methylated type1
traitfile=${output_450_dir}/${gse_number}/${gse_number}_T1_M_Signal.txt
outdir=${output_450_dir}/${gse_number}/
logFile=${output_450_dir}/${gse_number}/${gse_number}_T1_M_Signal_qqnorm.log
java -Xmx30g -Xms30g -jar ${jar_file} \
--mode normalize \
--in ${traitfile} \
--out ${outdir} \
--qqnorm | tee ${logFile}

# unmethylated type1
traitfile=${output_450_dir}/${gse_number}/${gse_number}_T1_U_Signal.txt
outdir=${output_450_dir}/${gse_number}/
logFile=${output_450_dir}/${gse_number}/${gse_number}_T1_U_Signal_qqnorm.log
java -Xmx30g -Xms30g -jar ${jar_file} \
--mode normalize \
--in ${traitfile} \
--out ${outdir} \
--qqnorm | tee ${logFile}

# methylated type1
traitfile=${output_450_dir}/${gse_number}/${gse_number}_T2_M_Signal.txt
outdir=${output_450_dir}/${gse_number}/
logFile=${output_450_dir}/${gse_number}/${gse_number}_T2_M_Signal_qqnorm.log
java -Xmx30g -Xms30g -jar ${jar_file} \
--mode normalize \
--in ${traitfile} \
--out ${outdir} \
--qqnorm | tee ${logFile}

# unmethylated type2
traitfile=${output_450_dir}/${gse_number}/${gse_number}_T2_U_Signal.txt
outdir=${output_450_dir}/${gse_number}
logFile=${output_450_dir}/${gse_number}/${gse_number}_T2_U_Signal_qqnorm.txt
java -Xmx30g -Xms30g -jar ${jar_file} \
--mode normalize \
--in ${traitfile} \
--out ${outdir} \
--qqnorm | tee ${logFile}
# =======================================================================================

# merge type1 & type2
ml Python
python ${code_dir}/merge_actions.py --gse $gse_number --action get_mvalues

# qqnorm
ml Java
jar_file=/home/p283190/methylation_network/eqtl-mapping-pipeline-1.4.7-SNAPSHOT/eqtl-mapping-pipeline.jar
traitfile=${mval_dir}/${gse_number}_MValues.tsv
outdir=${mval_dir}/${gse_number}
logFile=${mval_dir}/${gse_number}_qqnorm.log
java -Xmx50g -Xms50g -jar ${jar_file} \
--mode normalize \
--in ${traitfile} \
--out ${outdir} \
--qqnorm | tee ${logFile}

# remove the idat files