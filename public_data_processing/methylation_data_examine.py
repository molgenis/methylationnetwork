import numpy as np
from sklearn.decomposition import PCA
import pickle
import matplotlib.pyplot as plt
import pathlib
import pandas as pd

# # pca on all the data
# pca_onSamples = pickle.load(open("pca_onSamples.pickle.dat", "rb"))
# methylation = np.load("unique_public_450_values.QuantileNormalized.npy")
# # pcs_perCpg = pca_onSamples.transform(methylation)
# #
# # plt.figure(figsize=(10, 10))
# # plt.scatter(pcs_perCpg[:, 0], pcs_perCpg[:, 1])
# # plt.savefig("pcs_perCpgSite.png")
# # plt.close()
# #
# # plt.figure(figsize=(10, 10))
# # components = pca_onSamples.components_.T
# # plt.scatter(components[0, :], components[1, :])
# # plt.savefig("eigenVecs_perSample.png")
# # plt.close()
# #
# # pca_onCpgs = pickle.load(open("pca_onCpgs.pickle.dat", "rb"))
# # pcs_perSample = pca_onCpgs.transform(methylation.T)
# # components = pca_onCpgs.components_.T
# # plt.figure(figsize=(10, 10))
# # plt.scatter(pcs_perSample[:, 0], pcs_perSample[:, 1])
# # plt.savefig("pcs_perSample.png")
# # plt.close()
# #
# # plt.figure(figsize=(10, 10))
# # plt.scatter(components[0, :], components[1, :])
# # plt.savefig("eigenVecs_perCpg.png")
# # plt.close()
# #
# # means = np.mean(methylation, axis=1)
# # vars = np.var(methylation, axis=1)
# # sorted_means, sorted_vars = zip(*sorted(zip(means, vars), key=lambda x:x[0], reverse=True))
# # plt.errorbar(np.arange(len(means), means, vars))
# # plt.savefig("methylation_probes_mean_var.png")


qnormed_path = "/scratch/p283190/methylation/merged_mval/public_450_values.QuantileNormalized.npy"
print("Reading the data..." , flush=True)
start = t()
methylation  = np.load(qnormed_path)
print("Data loaded", t() - start, flush=True)
print("Running PCA...", flush=True)
start = t()
pca = PCA(svd_solver="randomized", n_components=10) # 10min
pca.fit(methylation)
print("Explained Variance.", pca.explained_variance_, flush=True)
print("PCA fitted.", t() - start, flush=True)
pickle.dump(pca, open("/scratch/p283190/methylation/merged_mval/pca_onSamples.pickle.dat", "wb"))
print("Saved PCA transformation.", flush=True)

pca_onSamples = pickle.load(open("/scratch/p283190/methylation/merged_mval/pca_onSamples.pickle.dat", "rb"))
components = pca_onSamples.components_.T
plt.scatter(components[0, :], components[1, :])
plt.savefig("/scratch/p283190/methylation/merged_mval/eigenVecs_perSample.png")
plt.close()

# 3 std from mean
eigenVector1 = components[:, 0]
sample_mean_pcs = np.mean(eigenVector1)
sample_std_pc1 = np.var(eigenVector1)**0.5
sample_outlier_index = np.where((eigenVector1 - sample_mean_pcs + 3* sample_std_pc1)<0)
methylation_valid = np.delete(methylation, sample_outlier_index[0], axis=1)
np.save("/scratch/p283190/methylation/merged_mval/unique_public_450_values.QuantileNormalized.3STDoutlierDeleted", methylation_valid)

# pca on clean data
# methylation_valid = np.load("/scratch/p283190/methylation/merged_mval/unique_public_450_values.QuantileNormalized.3STDoutlierDeleted.npy")
means_perCpg = np.mean(methylation_valid, axis=1)
stds_perCpg = np.var(methylation_valid, axis=1)

sorted_means_perCpg, sorted_stds_perCpg = zip(*sorted(zip(means_perCpg, stds_perCpg), key=lambda x:x[0], reverse=True))
plt.errorbar(np.arange(len(sorted_means_perCpg)), sorted_means_perCpg, sorted_stds_perCpg, alpha=0.2)
plt.savefig("/scratch/p283190/methylation/merged_mval/mean_std_perCpg_cleanedSample.png")
plt.close()

pca_onCleanSamples = PCA(svd_solver='randomized', n_components=10)
pca_onCleanSamples.fit(methylation_valid)
# pickle.dump(pca_onCleanSamples, open("/scratch/p283190/methylation/merged_mval/pca_onCleanSamples.pkl", "wb"))

pca_onCleanSamples = pickle.load(open("/scratch/p283190/methylation/merged_mval/pca_onCleanSamples.pkl", "rb"))
components = pca_onCleanSamples.components_.T
plt.scatter(components[:, 0], components[:, 1], alpha=0.2, edgecolors='gray', facecolors="None")
plt.savefig("/scratch/p283190/methylation/merged_mval/eigenVecs_onCleanSamples.png")
plt.close()

# todo: 1. delete -3std
# fit a gaussian distribution to the eigenvector1
pca_onSamples = pickle.load(open("/scratch/p283190/methylation/merged_mval/pca_onSamples.pickle.dat", "rb"))
components = pca_onSamples.components_.T
eigenVector1 = components[:, 0]
plt.hist(eigenVector1)
plt.savefig("/scratch/p283190/methylation/merged_mval/histogram_eigenVec1_onSamples.png")
plt.close()
# 3 std from mean
sample_mean_pcs = np.mean(eigenVector1)
sample_std_pc1 = np.var(eigenVector1)**0.5
sample_non_outlier_index = np.where((eigenVector1 - sample_mean_pcs + 3* sample_std_pc1)>=0)
methylation_valid = methylation[:, sample_non_outlier_index]
np.save("/scratch/p283190/methylation/merged_mval/unique_public_450_values.QuantileNormalized.3STDoutlierDeleted", methylation_valid)

columns_names = [item.strip() for item in
                 open("/scratch/p283190/methylation/merged_mval/unique_public_450_values.QuantileNormalized.cols.txt",
                      "r").readlines()]
valid_columns = []
for ind in sample_non_outlier_index[0]:
    valid_columns.append(columns_names[ind])
with open("/scratch/p283190/methylation/merged_mval/unique_public_450_values.QuantileNormalized.3STDoutlierDeleted.cols.txt", "w") as f:
    f.write("\n".join(valid_columns))

clean_sample_mean = np.mean(methylation_valid, axis=0)
clean_sample_var = np.var(methylation_valid, axis=0)
sorted_mean, sorted_var = zip(*sorted(zip(clean_sample_mean, clean_sample_var), key=lambda x:x[0],
                                      reverse=False))
plt.errorbar(np.arange(len(clean_sample_mean)), sorted_mean, sorted_var)
plt.title("mean and average methylation value per Sample")
plt.savefig("/scratch/p283190/methylation/merged_mval/mean_var_perCleanSample.png")
plt.close()


pca_onCleanSamples = PCA(svd_solver='randomized', n_components=100)
pca_onCleanSamples.fit(methylation_valid)
pickle.dump(pca_onCleanSamples, open("pca_onCleanSamples.pkl", "wb"))

# todo: color the outliers
data_dir=pathlib.Path("/scratch/p283190/methylation/merged_mval/")
pca_onSamples = pickle.load(open("/scratch/p283190/methylation/merged_mval/pca_onSamples.pickle.dat", "rb"))
col_names = [item.strip() for item in
                 open(data_dir/"unique_public_450_values.QuantileNormalized.3STDoutlierDeleted.cols.txt",
                      "r").readlines()]
eigenVectors_perSample = pca_onSamples.components_.T # sample * pcs should be 27k*100
eigenVectors_perSample_df = pd.DataFrame(data=eigenVectors_perSample,
                                         index=col_names,
                                         columns=[f"PC{ind}" for ind in range(eigenVectors_perSample.shape[1])])
all_columns = [item.strip() for item in
                 open(data_dir/"unique_public_450_values.cols.txt",
                      "r").readlines()]
valid_columns = set(col_names)
deleted_column = list(set(all_columns) - valid_columns)

outliers = eigenVectors_perSample_df.loc[deleted_column]
plt.figure(figsize=(5, 5))
plt.scatter(eigenVectors_perSample[:, 0], eigenVectors_perSample[:, 1], alpha=0.5)
plt.scatter(outliers[:, 0], outliers[:, 1], alpha=0.8, color='red')
plt.savefig(data_dir/"eigenvectors_outlier_in_red.png")
plt.close()