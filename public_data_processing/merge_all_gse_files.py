import pandas as pd
import os
import numpy as np


mval_directory = "/scratch/p283190/methylation/mval/"
gse_numbers = [item.strip() for item in
               open("/scratch/p283190/methylation/unique_gse_numbers.txt", "r").readlines()]

def get_gse_path(gse):
    path1 = os.path.join(mval_directory, gse, '{}_MValues.tsv.QuantileNormalized.txt.gz'.format(gse))
    path2 = os.path.join(mval_directory, gse,
                         '{}_MValues.tsv.ProbesWithZeroVarianceRemoved.QuantileNormalized.txt.gz'.format(gse))
    if os.path.exists(path1):
        return path1
    elif os.path.exists(path2):
        return path2
    else:
        raise IOError("{} does not exists.".format(gse))


def read_and_cut_gse(gse, valid_gse_index):
    gsepath = os.path.join(mval_directory, gse, '{}_MValues.tsv.QuantileNormalized.txt'.format(gse))
    gse_df = pd.read_csv(gsepath, sep="\t", index_col=0)
    gse_valid = gse_df.loc[valid_gse_index]
    return gse_valid.values


all_columns = []
gse_columns = []
for ind, gse in enumerate(gse_numbers):
    gse_path = get_gse_path(gse)
    gse_rows_path = os.path.join(mval_directory, gse, '{}.rownames.txt'.format(gse))
    gse_rows = set([item.strip() for item in open(gse_rows_path, 'r').readlines() if item.strip() not in ['-']])
    gse_col_path = os.path.join(mval_directory, gse, '{}.colnames.txt'.format(gse))
    gse_cols = [item.strip() for item in open(gse_col_path, 'r').readline().split("\t") if item.strip() not in ['-']]
    for col in gse_cols:
        if col not in all_columns:
            all_columns.append(col)
            gse_columns.append([gse, col])
    if ind  == 0:
        common_rows = gse_rows
    else:
        common_rows = common_rows & gse_rows


common_rows_list = list(common_rows)
with open(os.path.join(mval_directory, "public_450_values.rows.txt"), "w") as f:
    f.write("\n".join(common_rows_list))


with open(os.path.join(mval_directory, "public_450_values.cols.txt"), "w") as f:
    f.write("\n".join(all_columns))

with open(os.path.join(mval_directory, "public_450_values.gse_cols.txt"), "w") as f:
    f.write("\n".join(['\t'.join(item) for item in gse_columns]))


all_columns = [item.strip() for item in
               open(os.path.join(mval_directory, "public_450_values.cols.txt"), "r").readlines()]
print("In total", len(all_columns), " samples.", flush=True)
common_rows = [item.strip() for item in
               open(os.path.join(mval_directory, "public_450_values.rows.txt"), "r").readlines()]
print("In total", len(common_rows), " cpgsites.", flush=True)

all_values = np.zeros((len(common_rows), len(all_columns)), np.float) # 100GB

for ind, gse in enumerate(gse_numbers):
    gse_valid_values = read_and_cut_gse(gse, common_rows)
    if ind == 0:
        col_start_ind = 0
        col_end_ind = gse_valid_values.shape[1]
    else:
        col_start_ind = col_end_ind
        col_end_ind = col_start_ind + gse_valid_values.shape[1]
    all_values[:, col_start_ind:col_end_ind] = gse_valid_values

print("all_values has shape", all_values.shape, flush=True)
np.save(os.path.join(mval_directory, "public_450_values"), all_values)
print("Saved in path:", os.path.join(mval_directory, "public_450_values.npy"))