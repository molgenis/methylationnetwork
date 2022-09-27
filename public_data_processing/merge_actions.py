import pandas as pd
import numpy as np
import argparse
import os


def merge_type1_red_green(gse):
    type1_red_m_path = "/scratch/p283190/methylation/output_450/%s/%s_T1_Red_M_Signal.txt"%(gse, gse)
    type1_green_m_path = "/scratch/p283190/methylation/output_450/%s/%s_T1_Grn_M_Signal.txt"%(gse, gse)
    type1_red_u_path = "/scratch/p283190/methylation/output_450/%s/%s_T1_Red_U_Signal.txt"%(gse, gse)
    type1_green_u_path = "/scratch/p283190/methylation/output_450/%s/%s_T1_Grn_U_Signal.txt"%(gse, gse)
    # load the data
    print("Loading the red methylated channel...", flush=True)
    type1_red_m = pd.read_csv(type1_red_m_path, sep="\t", index_col=0)
    print("Loading the green methylated channel...", flush=True)
    type1_green_m = pd.read_csv(type1_green_m_path, sep="\t", index_col=0)
    print("Loading the red unmethylated channel...", flush=True)
    type1_red_u = pd.read_csv(type1_red_u_path, sep="\t", index_col=0)
    print("Loading the green unmethylated channel...", flush=True)
    type1_green_u = pd.read_csv(type1_green_u_path, sep="\t", index_col=0)
    # merge
    merge_type1_m = pd.concat([type1_red_m, type1_green_m], axis=0)
    merge_type1_u = pd.concat([type1_red_u, type1_green_u], axis=0)
    merged_type1_m_path = "/scratch/p283190/methylation/output_450/%s/%s_T1_M_Signal.txt"%(gse, gse)
    merged_type1_u_path = "/scratch/p283190/methylation/output_450/%s/%s_T1_U_Signal.txt"%(gse, gse)
    merge_type1_m.to_csv(merged_type1_m_path, sep="\t")
    print("Type1 methylated values saved in %s"%merged_type1_m_path)
    merge_type1_u.to_csv(merged_type1_u_path, sep="\t")
    print("Type1 unmethylated values saved in %s"%merged_type1_u_path)
    return None


def get_normalized_path(gse, name):
    if os.path.exists("/scratch/p283190/methylation/output_450/%s/%s.QuantileNormalized.txt.gz" % (gse, name)):
      return "/scratch/p283190/methylation/output_450/%s/%s.QuantileNormalized.txt.gz" % (gse, name)
    elif os.path.exists("/scratch/p283190/methylation/output_450/%s/%s.ProbesWithZeroVarianceRemoved.QuantileNormalized.txt.gz" % (gse, name)):
        return "/scratch/p283190/methylation/output_450/%s/%s.ProbesWithZeroVarianceRemoved.QuantileNormalized.txt.gz" % (gse, name)
    else:
        raise FileNotFoundError('Check %s'%gse)


def merge_type1_type2(gse):
    type1_m_path = get_normalized_path(gse, "%s_T1_M_Signal"%gse)
    type1_u_path = get_normalized_path(gse, "%s_T1_U_Signal"%gse)
    type2_m_path = get_normalized_path(gse, "%s_T2_M_Signal"%gse)
    type2_u_path = get_normalized_path(gse, "%s_T2_U_Signal"%gse)
    type1_m = pd.read_csv(type1_m_path, sep="\t", compression="gzip", index_col=0)
    type1_u = pd.read_csv(type1_u_path, sep="\t", compression="gzip", index_col=0)
    type2_m = pd.read_csv(type2_m_path, sep="\t", compression="gzip", index_col=0)
    type2_u = pd.read_csv(type2_u_path, sep="\t", compression="gzip", index_col=0)
    m = pd.concat([type1_m, type2_m], axis=0)
    print("Merged type1 and type2 methylated values.", flush=True)
    u = pd.concat([type1_u, type2_u], axis=0)
    print("Merged type1 and type 2 unmethylated values.", flush=True)
    # m.to_csv("/scratch/p283190/methylation/output_450/%s/%s_M.tsv", sep="\t")
    # u.to_csv("/scratch/p283190/methylation/output_450/%s/%s_U.tsv", sep="\t")
    return m, u


def calculate_MValues(m, u):
    m_values = m.values.clip(min=0)
    u_values = u.values.clip(min=0)
    m_values = np.nan_to_num(m_values)
    u_values= np.nan_to_num(u_values)
    mvalues = np.log2((m_values + 1) / (u_values + 1))
    mvalues_df = pd.DataFrame(data=mvalues, index=m.index, columns=m.columns)
    mvalues_df.to_csv("/scratch/p283190/methylation/mval/%s_MValues.tsv"%gse, sep="\t")
    print("MValues saved to /scratch/p283190/methylation/mval/%s_MValues.tsv"%gse, flush=True)
    return None


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gse", dest="gse", type=str)
    parser.add_argument("--action", dest="action", type=str)
    return parser.parse_args()

arguments = parseArguments()
gse = arguments.gse
action = arguments.action

output_dir = os.path.join("/scratch/p283190/methylation/output_450/%s"%gse)
if action == 'merge_green_red':
    merge_type1_red_green(gse)
elif action == 'get_mvalues':
    m, u = merge_type1_type2(gse)
    calculate_MValues(m, u)
else:
    raise NameError("Please enter either merge_green_red or get_mvalues")