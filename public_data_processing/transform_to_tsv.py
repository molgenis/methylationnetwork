import pandas as pd
import numpy as np
import argparse


def read_npy_to_df(path_prefix):
    '''
    This reads the numpy file and its corresponding rows and columns into a dataframe
    :param path_prefix: string
    :return: pandas dataframe
    '''
    data = np.load(f'{path_prefix}.npy')
    rows = [item for item in open(f'{path_prefix}.rows.txt', 'r').readlines()]
    cols = [item for item in open(f'{path_prefix}.cols.txt', 'r').readlines()]
    return pd.DataFrame(data=data, index=rows, columns=cols)


def save_df_to_tsv_gz(path_prefix, save_prefix):
    '''
    This reads the numpy files and its corresponding rows and columns and saves it into a gzipped tsv file
    :param path_prefix:
    :param save_prefix:
    :return:
    '''
    df = read_npy_to_df(path_prefix)
    df.to_csv(f'{save_prefix}.tsv.gz', sep='\t', compression='gzip')
    return None


def argumentsparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_prefix', type=str, dest='path_prefix')
    parser.add_argument('--save_prefix', type=str, dest='save_prefix')
    return parser


def main():
    args = argumentsparser().parse_args()
    path_prefix, save_prefix = args.path_prefix, args.save_prefix
    print(f"Reading numpy file {path_prefix}.npy\nRows in f{path_prefix}.rows.txt\nColumns in f{path_prefix}.cols.txt")
    print(f"Saving file in {save_prefix}.tsv.gz")
    save_df_to_tsv_gz(path_prefix, save_prefix)


if __name__ == '__main__':
    main()
