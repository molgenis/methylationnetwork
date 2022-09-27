#!/usr/bin/env bash
#SBATCH --time=5:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=30gb
#SBATCH --nodes=1
#SBATCH --get-user-env=L


# test file
gse_number=$1
ftp_link=$2

source_dir=/scratch/p283190/methylation
code_dir=/home/p283190/methylation_network/scripts

raw_data_dir=${source_dir}/raw
idat_dir=${source_dir}/idat
output_450_dir=${source_dir}/output_450


echo "Processing "${gse_number}

echo "Downloading..."
mkdir -p ${raw_data_dir}/${gse_number}
mkdir -p ${idat_dir}/${gse_number}/project_${gse_number}
mkdir -p ${output_450_dir}/${gse_number}
wget -O ${raw_data_dir}/${gse_number}/${gse_number}_RAW.tar -d --header="X-Auth-Token: ed03bd954ebbdf61ad62f0996b43b5d23408" ${ftp_link}/suppl/${gse_number}_RAW.tar
tar -xvf ${raw_data_dir}/${gse_number}/${gse_number}_RAW.tar -C ${raw_data_dir}/${gse_number}/

echo "Checking and replacing IDAT with idat..."
# check if we have idat files now.. replace uppercase IDAT
uppercasecount=$(find ${raw_data_dir}/${gse_number} -mindepth 1 -type f -name "*.IDAT" -printf x | wc -c)
if [ ${uppercasecount} -gt 0 ]
then
  # file names are uppercase
  rename 's/\.IDAT$/\.idat/' *.IDAT
fi

# unzip to idat
count=$(find ${raw_data_dir}/${gse_number}/ -name "*.idat.gz" | wc -l)
echo "Unzipping downloaded ${count} idat files..."
for filename in ${raw_data_dir}/${gse_number}/*.idat.gz; do
  filename_base=$(basename -- "$filename")
  f="${filename_base%.idat.gz}"
  echo ${f}
  gzip -dc ${filename} > ${idat_dir}/${gse_number}/project_${gse_number}/${f}.idat
  rm ${filename}
done

if [ -f "/data/p283190/gsm_platforms/uuid_${gse_number}_platforms.txt" ]
then
python ${code_dir}/select_450k_smaples.py --gse ${gse_number}
fi
rm $(find ${idat_dir}/${gse_number}/project_${gse_number}/ -type f -size +10M)


# ===================== 450k pipeline ==========================
mkdir -p ${output_450_dir}/${gse_number}
ml R
nice -n20 Rscript \
${code_dir}/slimmedPipeline.450K.noSubprojects.R \
${idat_dir}/${gse_number}/ \
${output_450_dir}/${gse_number}/ \
${gse_number}

if [ -f "${output_450_dir}/${gse_number}/${gse_number}_T1_Red_M_Signal.txt" ];
then
rm ${idat_dir}/${gse_number}/project_${gse_number}/*
fi
# ==============================================================
