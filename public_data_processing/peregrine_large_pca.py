import numpy as np
from sklearn.decomposition import PCA
import pickle
from time import time as t
# import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import argparse


# def draw_mean_std(data, axis, title, fig_savepath):
#     startime = t()
#     print("Calculating means and std...", flush=True)
#     means = np.mean(data, axis=axis)
#     stds = np.std(data, axis = axis)
#     print("Mean and std calculated, using time", t() - startime, flush=True)
#     sorted_means, sorted_stds = zip(*sorted(zip(means, stds), key=lambda x:x[0]))
#     plt.errorbar(np.arange(len(means)), sorted_means, sorted_stds)
#     plt.title(title)
#     plt.savefig(fig_savepath)
#     plt.close()
#     return None


def perform_pca(data, n_components, pca_savepath):
    # first standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    pca = PCA(svd_solver='randomized', n_components=n_components)
    print("Fitting pca...", flush=True)
    startime = t()
    pca.fit(scaled_data)
    print("PCA fitted, time:", t() - startime, flush=True)
    pickle.dump(pca, open(pca_savepath, "wb"))
    print("PCA saved.", flush=True)
    # startime = t()
    # print("Transforming data..", flush=True)
    # transformed_data = pca.transform(data)
    # print("Data transformed, time", t() - startime, flush=True)
    # np.save("/scratch/p283190/methylation/merged_mval/pcs_per_individual", transformed_data)
    return pca

def read_data_pca_draw(npy_data_path,
                       mean_std_perRow_fig_path,mean_std_perCol_fig_path,
                       whether_perform_pca = False, n_components=10, pca_path=None,
                       row_name="Cpgsite", col_name="Individual", eigenVectors12_figpath=None):
    startime = t()
    print("Loading data..", flush=True)
    data = np.load(npy_data_path).T # transposed data, sample * cpgsites
    print("Data loaded with shape, ", data.shape, "Using time: ", t() - startime, flush=True)
    _ = perform_pca(data, n_components, pca_path)
    # if whether_perform_pca:
    #     perform_pca(data, n_components, pca_path)
    # if mean_std_perCol_fig_path:
    #     draw_mean_std(data, axis=0, title=f"per {col_name}", fig_savepath=mean_std_perCol_fig_path)
    # if mean_std_perRow_fig_path:
    #     draw_mean_std(data, axis=1, title=f"per {row_name}", fig_savepath=mean_std_perRow_fig_path)
    # if eigenVectors12_figpath:
    #     eigenVectors_drawing(eigenVectors12_figpath, pca_path=pca_path)
    return None


# def eigenVectors_drawing(eigenVectors12_figpath, pca=None, pca_path=None):
#     if pca_path:
#         pca = pickle.load(open(pca_path , "rb"))
#     components = pca.components_.T
#     plt.figure(figsize=(10, 10))
#     plt.scatter(components[:, 0], components[:, 1], alpha=0.5)
#     plt.xlabel("Eigen vector 1")
#     plt.ylabel("Eigen vector 2")
#     plt.savefig(eigenVectors12_figpath)
#     return None


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--npy_path", dest='npy_path')
argument_parser.add_argument("--perform_pca", dest='whether_pca', type=bool)
argument_parser.add_argument("--n_components", dest='n_components')
argument_parser.add_argument("--pca_path", dest='pca_path')
argument_parser.add_argument("--mean_std_perRow_fig_path", dest='mean_std_perRow_fig_path')
argument_parser.add_argument("--mean_std_perCol_fig_path", dest='mean_std_perCol_fig_path')
argument_parser.add_argument("--row_name", dest='row_name')
argument_parser.add_argument("--col_name", dest='col_name')
argument_parser.add_argument("--eigenVectors12_figpath", dest='eigenVectors12_figpath')
arguments = argument_parser.parse_args()

read_data_pca_draw(arguments.npy_path,
                   arguments.mean_std_perRow_fig_path,arguments.mean_std_perCol_fig_path,
                   whether_perform_pca = arguments.whether_pca, n_components=int(arguments.n_components),
                   pca_path=arguments.pca_path,
                   row_name=arguments.row_name, col_name=arguments.col_name,
                   eigenVectors12_figpath=arguments.eigenVectors12_figpath)


#
# # transposed data pca
# print("Transposing data...", flush=True)
# transposed = qnormed_data.T
# print("Running PCA on transposed data...", flush=True)
# start = t()
# pca = PCA(svd_solver="randomized", n_components=100)
# pca.fit(transposed)
# print("Explained Variance.", pca.explained_variance_[:10], flush=True)
# print("PCA fitted.", t() - start, flush=True)
# pickle.dump(pca, open("/scratch/p283190/methylation/merged_mval/pca_onCpgs.pickle.dat", "wb"))
# print("Saved PCA transformation.", flush=True)
# np.save("/scratch/p283190/methylation/merged_mval/PCs_pcaOnCpgs", pca.components_)
# print("Saved PCA components", flush=True)
#
#
# means = np.mean(qnormed_data, axis=0)
# stds = np.var(qnormed_data, axis=0)
# sorted_means, sorted_stds = zip(*sorted(zip(means, stds), key=lambda x:x[0], reverse=True))
# >>> np.var(means)
# 7.220311181930494e-13
# >>> np.mean(means)
# -0.29431165722544761
# >>> np.mean(stds)
# 8.2215511514511856
# >>> np.var(stds)
# 2.7212981220881889e-10
# >>> qnormed_data[:10, :5]
# array([[-1.48309524, -1.81550673, -1.68536216, -1.44155086, -1.36481826],
#        [-3.7676742 , -3.93200267, -4.00661086, -3.9355714 , -4.05272884],
#        [ 0.70181205,  0.81239692,  0.28958146,  1.0202973 ,  0.72849177],
#        [ 3.01854582,  3.39456906,  2.82828632,  2.96365074,  2.98422006],
#        [-3.60768036, -3.2907522 , -3.61327999, -3.49299449, -3.10759155],
#        [-2.88553673, -2.82392855, -3.22074268, -2.89953966, -3.93119046],
#        [ 4.37578521,  3.42461586,  3.90152382,  4.13895324,  3.59503849],
#        [-2.6994018 , -2.31370818, -3.04628428, -2.95304594, -2.69560367],
#        [ 1.96484923,  1.4743009 ,  1.45425474,  1.7718447 ,  1.41897692],
#        [ 2.47989758,  2.79947477,  2.67199375,  2.57673484,  2.79303614]])
# >>> qnormed_data.shape
# (422803, 27791)


